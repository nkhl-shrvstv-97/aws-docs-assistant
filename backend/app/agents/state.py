from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # Holds conversation history and intermediate agent responses
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    # The search-optimized version of the user's latest query
    standalone_query: str
    
    # Context chunks retrieved from Local RAG or Live Search
    documents: list[dict]  # dict contains: content, source_url, title
    
    # The final generated response text
    generation: str
    
    # Internal routing flags
    search_needed: bool
    is_aws_related: bool
    classification: str
    web_search_run: bool
    
    # Guard against infinite loops
    loop_count: int
