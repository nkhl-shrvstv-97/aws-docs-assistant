import json
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage
from backend.app.config import settings
from backend.app.agents.state import AgentState
from backend.app.agents.prompts import CLASSIFY_DOMAIN_PROMPT

def classify_domain(state: AgentState) -> dict:
    """
    Classify whether the user query is related to AWS.
    """
    print("--- NODE: CLASSIFY DOMAIN ---")
    messages = state.get("messages", [])
    if not messages:
        return {"is_aws_related": False}
    
    last_msg = messages[-1].content
    history_str = "\n".join([f"{type(m).__name__}: {m.content}" for m in messages[:-1]])
    
    prompt = CLASSIFY_DOMAIN_PROMPT.format(history=history_str, query=last_msg)
    
    llm = ChatBedrock(
        model_id=settings.BEDROCK_CLASSIFY_MODEL_ID,
        region_name=settings.AWS_REGION
    )
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        content = response.content.strip()
        # Clean up any potential markdown backticks
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        data = json.loads(content)
        is_aws_related = data.get("is_aws_related", True)
    except Exception as e:
        print(f"Error in classify_domain: {e}")
        # Default to True so we don't refuse valid questions in case of errors
        is_aws_related = True
        
    return {"is_aws_related": is_aws_related, "loop_count": 0}
