from backend.app.agents.state import AgentState
from backend.app.db.session import SessionLocal
from backend.app.tools.vector_store import similarity_search

def retrieve_local(state: AgentState) -> dict:
    """
    Retrieve relevant documents from PostgreSQL pgvector store.
    """
    print("--- NODE: RETRIEVE LOCAL ---")
    query = state.get("standalone_query")
    if not query:
        return {"documents": []}
        
    print(f"Retrieving for: {query}")
    try:
        with SessionLocal() as db:
            results = similarity_search(db, query, limit=5)
            
        formatted_docs = []
        for r in results:
            formatted_docs.append({
                "content": r.get("content"),
                "source_url": r.get("source_url"),
                "title": r.get("title")
            })
            
        print(f"Retrieved {len(formatted_docs)} documents.")
        return {"documents": formatted_docs}
    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return {"documents": []}
