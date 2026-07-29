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
    # Check output of grade_generation
    # Wait, the node outputs a dict with is_grounded. Let's make sure it's correct.
    # Note: We can also pass state directly or read from state.
    # We will compute is_grounded inside a local check or reuse the key if set in state/return.
    # Let's check state values.
    loop_count = state.get("loop_count", 0)
    
    # We will call the grader directly here or use its result. Since in LangGraph we have the node,
    # the node should update the state. Let's check state's properties.
    # To keep state clean, let's look up if the last grounding run set a flag.
    # Or we can just invoke the grading check. Let's inspect state:
    # We can write a custom condition.
    # Let's import the grader here to run synchronously as a router, or run in the node.
    # Since grade_generation was run as a node, we should store its result in state.
    # Let's assume we modify AgentState to contain `is_grounded` or we just run the grade_generation check here.
    # Let's run it directly here to keep the state clean, or read it from state.
    # To read from state, we can add `is_grounded` to state or return it from Node 6.
    # Let's run the grounding check in route_grounding or read it. Let's check.
    # If we run it in route_grounding, it's very easy:
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
            "generate_answer": "generate_answer"
        }
    )
    
    # Compile Graph
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)

agent_graph = build_agent_graph()
