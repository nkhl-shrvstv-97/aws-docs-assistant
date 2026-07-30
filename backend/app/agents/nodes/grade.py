import json
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage
from backend.app.config import settings
from backend.app.agents.state import AgentState
from backend.app.agents.prompts import DOCUMENT_GRADER_PROMPT, GROUNDING_GRADER_PROMPT

def grade_documents(state: AgentState) -> dict:
    """
    Filter retrieved documents using Bedrock to evaluate relevance.
    """
    print("--- NODE: GRADE DOCUMENTS ---")
    query = state.get("standalone_query")
    documents = state.get("documents", [])
    
    if not query or not documents:
        return {"documents": [], "search_needed": True}
        
    llm = ChatBedrock(
        model_id=settings.BEDROCK_CLASSIFY_MODEL_ID,
        region_name=settings.AWS_REGION
    )
    
    filtered_docs = []
    
    for doc in documents:
        prompt = DOCUMENT_GRADER_PROMPT.format(query=query, document=doc["content"])
        try:
            response = llm.invoke([HumanMessage(content=prompt)])
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            res = json.loads(content)
            if res.get("relevant", True):
                filtered_docs.append(doc)
        except Exception as e:
            print(f"Error grading document: {e}")
            # Do not append in case of error to be strict and allow web search fallback
            
    search_needed = len(filtered_docs) == 0
    print(f"Docs after grading: {len(filtered_docs)} / {len(documents)}. Search needed: {search_needed}")
    return {"documents": filtered_docs, "search_needed": search_needed}

def grade_generation(state: AgentState) -> dict:
    """
    Determine if the generation is grounded in the documents.
    """
    print("--- NODE: GRADE GENERATION ---")
    generation = state.get("generation")
    documents = state.get("documents", [])
    
    if not generation:
        return {"is_grounded": False}
        
    if not documents:
        # If there are no documents, we can't ground it
        return {"is_grounded": True}
        
    llm = ChatBedrock(
        model_id=settings.BEDROCK_CLASSIFY_MODEL_ID,
        region_name=settings.AWS_REGION
    )
    
    context_str = "\n\n".join([f"Source: {d['source_url']}\n{d['content']}" for d in documents])
    prompt = GROUNDING_GRADER_PROMPT.format(context=context_str, generation=generation)
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        res = json.loads(content)
        is_grounded = res.get("grounded", True)
    except Exception as e:
        print(f"Error grading generation: {e}")
        is_grounded = True
        
    print(f"Grounding check: {is_grounded}")
    return {"is_grounded": is_grounded}
