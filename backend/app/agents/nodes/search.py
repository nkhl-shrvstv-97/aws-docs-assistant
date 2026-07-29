from backend.app.agents.state import AgentState
from backend.app.tools.doc_search import search_aws_docs

def live_aws_search(state: AgentState) -> dict:
    """
    Query live AWS documentation using the search tool.
    """
    print("--- NODE: LIVE AWS SEARCH ---")
    query = state.get("standalone_query")
    if not query:
        return {}
        
    results = search_aws_docs(query, limit=3)
    
    current_docs = state.get("documents", []) or []
    # Combine existing documents with new search results
    all_docs = list(current_docs) + results
    
    print(f"Appended {len(results)} live search documents. Total docs: {len(all_docs)}")
    return {"documents": all_docs}
