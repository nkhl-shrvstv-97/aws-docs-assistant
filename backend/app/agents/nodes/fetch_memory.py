from sqlalchemy import text
from backend.app.agents.state import AgentState
from backend.app.db.session import SessionLocal
from backend.app.tools.vector_store import get_embedding

def fetch_session_summary(state: AgentState) -> dict:
    """
    Look up past session summaries using cosine similarity on standalone_query.
    """
    print("--- NODE: FETCH SESSION SUMMARY ---")
    query = state.get("standalone_query")
    if not query:
        return {}
        
    try:
        query_embedding = get_embedding(query)
        emb_str = f"[{','.join(map(str, query_embedding))}]"
        
        sql = text("""
            SELECT session_id, summary, topics, (embedding <=> :query_embedding) AS distance
            FROM session_summaries
            ORDER BY distance ASC
            LIMIT 2
        """)
        
        with SessionLocal() as db:
            result = db.execute(sql, {"query_embedding": emb_str})
            rows = [dict(row._mapping) for row in result]
            
        current_docs = state.get("documents", []) or []
        memory_docs = []
        for row in rows:
            # We treat past summaries as a document to inject context
            memory_docs.append({
                "content": f"Past conversation summary for session {row['session_id']}: {row['summary']}. Topics covered: {', '.join(row['topics'])}",
                "source_url": f"session-memory://{row['session_id']}",
                "title": f"Past Session Memory {row['session_id']}"
            })
            
        print(f"Fetched {len(memory_docs)} past session summaries.")
        return {"documents": current_docs + memory_docs}
    except Exception as e:
        print(f"Error fetching session summary: {e}")
        return {}
