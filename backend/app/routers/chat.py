import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from langchain_aws import ChatBedrock
from backend.app.agents.graph import agent_graph
from backend.app.config import settings
from backend.app.db.session import SessionLocal
from backend.app.db.models import SessionSummary
from backend.app.tools.vector_store import get_embedding

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str
    thread_id: str

class ChatResponse(BaseModel):
    response: str
    standalone_query: str
    is_aws_related: bool
    sources: list[dict]

class EndSessionRequest(BaseModel):
    thread_id: str

class EndSessionResponse(BaseModel):
    message: str
    summary: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint to send message to the RAG Agent.
    """
    config = {"configurable": {"thread_id": request.thread_id}}
    
    try:
        initial_state = {
            "messages": [HumanMessage(content=request.prompt)],
            "loop_count": 0
        }
        
        final_state = await agent_graph.ainvoke(initial_state, config=config)
        
        generation = final_state.get("generation", "")
        standalone_query = final_state.get("standalone_query", "")
        is_aws_related = final_state.get("is_aws_related", True)
        
        documents = final_state.get("documents", []) or []
        sources = []
        for doc in documents:
            if not doc.get("source_url", "").startswith("session-memory://"):
                sources.append({
                    "title": doc.get("title"),
                    "url": doc.get("source_url")
                })
        
        unique_sources = []
        seen_urls = set()
        for src in sources:
            if src["url"] not in seen_urls:
                seen_urls.add(src["url"])
                unique_sources.append(src)
                
        return ChatResponse(
            response=generation,
            standalone_query=standalone_query,
            is_aws_related=is_aws_related,
            sources=unique_sources
        )
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/end-session", response_model=EndSessionResponse)
async def end_session_endpoint(request: EndSessionRequest):
    """
    Summarize current session history and write summary/embedding to the DB.
    """
    config = {"configurable": {"thread_id": request.thread_id}}
    try:
        # Retrieve graph history state
        state = agent_graph.get_state(config)
        messages = state.values.get("messages", []) if state else []
        
        if not messages:
            return EndSessionResponse(message="No session history found to summarize.", summary="")
            
        # Format messages for prompt
        history_str = "\n".join([f"{type(m).__name__}: {m.content}" for m in messages])
        
        # Summarize using Haiku
        llm = ChatBedrock(
            model_id=settings.BEDROCK_CLASSIFY_MODEL_ID,
            region_name=settings.AWS_REGION
        )
        
        summary_prompt = f"""You are a conversation summarization helper.
Review the following conversation history between a user and an AWS docs assistant.
Produce a concise summary of the topics discussed and key solutions provided.
Also output a JSON object containing the summary and key topic strings.

Format raw JSON only as:
{{"summary": "A concise summary here...", "topics": ["topic1", "topic2"]}}

Conversation:
{history_str}
"""
        response = llm.invoke([HumanMessage(content=summary_prompt)])
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        res = json.loads(content)
        summary = res.get("summary", "Conversational session.")
        topics = res.get("topics", ["AWS"])
        
        # Get embedding of summary
        summary_embedding = get_embedding(summary)
        
        # Write to PostgreSQL DB
        with SessionLocal() as db:
            # Check if summary already exists for this session
            existing = db.query(SessionSummary).filter(SessionSummary.session_id == request.thread_id).first()
            if existing:
                existing.summary = summary
                existing.topics = topics
                existing.embedding = summary_embedding
            else:
                new_summary = SessionSummary(
                    session_id=request.thread_id,
                    summary=summary,
                    topics=topics,
                    embedding=summary_embedding
                )
                db.add(new_summary)
            db.commit()
            
        return EndSessionResponse(
            message="Session successfully summarized and saved to database memory.",
            summary=summary
        )
    except Exception as e:
        print(f"Error in end_session_endpoint: {e}")
        # Return success with warning or raise 500
        raise HTTPException(status_code=500, detail=str(e))
