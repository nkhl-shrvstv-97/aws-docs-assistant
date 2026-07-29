from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage
from backend.app.config import settings
from backend.app.agents.state import AgentState
from backend.app.agents.prompts import ANSWER_GENERATOR_PROMPT

def generate_answer(state: AgentState) -> dict:
    """
    Synthesize final response from context and history using Claude 3.5 Sonnet.
    """
    print("--- NODE: GENERATE ANSWER ---")
    documents = state.get("documents", [])
    messages = state.get("messages", [])
    loop_count = state.get("loop_count", 0)
    
    if not messages:
        return {"generation": ""}
        
    last_msg = messages[-1].content
    history_str = "\n".join([f"{type(m).__name__}: {m.content}" for m in messages[:-1]])
    
    # Format documents as content string
    context_str = ""
    if documents:
        for idx, doc in enumerate(documents):
            context_str += f"\nDocument [{idx+1}]: {doc.get('title')}\nSource URL: {doc.get('source_url')}\nContent: {doc.get('content')}\n---"
    else:
        context_str = "No relevant AWS documents found in context database."
        
    prompt = ANSWER_GENERATOR_PROMPT.format(
        context=context_str,
        history=history_str,
        query=last_msg
    )
    
    llm = ChatBedrock(
        model_id=settings.BEDROCK_GENERATE_MODEL_ID,
        region_name=settings.AWS_REGION
    )
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        generation = response.content.strip()
    except Exception as e:
        print(f"Error in generate_answer: {e}")
        generation = "I encountered an error generating an answer from Amazon Bedrock."
        
    return {"generation": generation, "loop_count": loop_count + 1}
