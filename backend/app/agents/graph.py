from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from backend.app.agents.state import AgentState
from backend.app.agents.nodes.classify import classify_domain
from backend.app.agents.nodes.refuse import refuse_out_of_scope
from backend.app.agents.nodes.rewrite import rewrite_query
from backend.app.agents.nodes.fetch_memory import fetch_session_summary
from backend.app.agents.nodes.retrieve import retrieve_local
from backend.app.agents.nodes.grade import grade_documents, grade_generation
from backend.app.agents.nodes.search import live_aws_search
from backend.app.agents.nodes.generate import generate_answer

# Conditional router for classify_domain
def route_domain(state: AgentState) -> str:
    if state.get("is_aws_related", True):
        return "rewrite_query"
    return "refuse_out_of_scope"

# Conditional router for rewrite_query
def route_history(state: AgentState) -> str:
    query = state.get("standalone_query", "").lower()
    keywords = ["previous", "last", "session", "yesterday", "earlier", "history", "before", "past"]
    if any(k in query for k in keywords):
        return "fetch_session_summary"
    return "retrieve_local"

# Conditional router for grade_documents
def route_search(state: AgentState) -> str:
    if state.get("search_needed", False):
        return "live_aws_search"
    return "generate_answer"

# Conditional router for grade_generation
def route_grounding(state: AgentState) -> str:
    loop_count = state.get("loop_count", 0)
    generation = state.get("generation", "").lower()
    web_search_run = state.get("web_search_run", False)
    
    # Check if final generation is a refusal to answer due to missing context
    refusal_phrases = ["cannot answer", "do not have enough information", "does not contain any information", "no relevant aws documents"]
    is_refusal = any(phrase in generation for phrase in refusal_phrases)
    
    # If it is a refusal and we haven't done a web search yet, route to live_aws_search
    if is_refusal and not web_search_run:
        print("--- ROUTER: Refusal detected and web search has not run yet. Routing to live_aws_search ---")
        return "live_aws_search"
        
    from backend.app.agents.nodes.grade import grade_generation as check_grounding
    res = check_grounding(state)
    is_grounded = res.get("is_grounded", True)
    
    if is_grounded or loop_count >= 3:
        return END
    return "generate_answer"

def build_agent_graph():
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("classify_domain", classify_domain)
    workflow.add_node("refuse_out_of_scope", refuse_out_of_scope)
    workflow.add_node("rewrite_query", rewrite_query)
    workflow.add_node("fetch_session_summary", fetch_session_summary)
    workflow.add_node("retrieve_local", retrieve_local)
    workflow.add_node("grade_documents", grade_documents)
    workflow.add_node("live_aws_search", live_aws_search)
    workflow.add_node("generate_answer", generate_answer)
    
    # Set Entry Point
    workflow.set_entry_point("classify_domain")
    
    # Add Edges
    workflow.add_conditional_edges(
        "classify_domain",
        route_domain,
        {
            "rewrite_query": "rewrite_query",
            "refuse_out_of_scope": "refuse_out_of_scope"
        }
    )
    
    workflow.add_edge("refuse_out_of_scope", END)
    
    workflow.add_conditional_edges(
        "rewrite_query",
        route_history,
        {
            "fetch_session_summary": "fetch_session_summary",
            "retrieve_local": "retrieve_local"
        }
    )
    
    workflow.add_edge("fetch_session_summary", "retrieve_local")
    
    workflow.add_conditional_edges(
        "grade_documents",
        route_search,
        {
            "live_aws_search": "live_aws_search",
            "generate_answer": "generate_answer"
        }
    )
    
    workflow.add_edge("retrieve_local", "grade_documents")
    workflow.add_edge("live_aws_search", "generate_answer")
    
    workflow.add_conditional_edges(
        "generate_answer",
        route_grounding,
        {
            END: END,
            "generate_answer": "generate_answer",
            "live_aws_search": "live_aws_search"
        }
    )
    
    # Compile Graph
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)

agent_graph = build_agent_graph()
