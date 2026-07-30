from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage
from backend.app.config import settings
from backend.app.agents.state import AgentState
from backend.app.agents.prompts import QUERY_REWRITER_PROMPT

def rewrite_query(state: AgentState) -> dict:
    """
    Synthesize user query and chat history into a standalone vector search query.
    """
    print("--- NODE: REWRITE QUERY ---")
    messages = state.get("messages", [])
    if not messages:
        return {"standalone_query": ""}
        
    last_msg = messages[-1].content
    history_str = "\n".join([f"{type(m).__name__}: {m.content}" for m in messages[:-1]])
    
    # If history is empty, simply use the last message
    if not history_str:
        return {"standalone_query": last_msg}
        
    prompt = QUERY_REWRITER_PROMPT.format(history=history_str, query=last_msg)
    
    llm = ChatBedrock(
        model_id=settings.BEDROCK_CLASSIFY_MODEL_ID,
        region_name=settings.AWS_REGION
    )
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        standalone = response.content.strip()
    except Exception as e:
        print(f"Error in rewrite_query: {e}")
        standalone = last_msg
        
    print(f"Standalone Query: {standalone}")
    return {"standalone_query": standalone}
