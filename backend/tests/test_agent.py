import pytest
from unittest.mock import MagicMock, patch
from langchain_core.messages import HumanMessage, AIMessage
from backend.app.agents.state import AgentState
from backend.app.agents.nodes.refuse import refuse_out_of_scope
from backend.app.agents.nodes.classify import classify_domain
from backend.app.agents.graph import route_domain, route_history, route_search

def test_refuse_node():
    # Out of scope query
    state: AgentState = {"messages": [HumanMessage(content="Hello")], "classification": "out_of_scope"}
    res = refuse_out_of_scope(state)
    assert "I am an AI assistant dedicated to helping with AWS Documentation" in res["generation"]

    # Greeting pleasantry
    state_greeting: AgentState = {"messages": [HumanMessage(content="Hi there!")], "classification": "conversational"}
    res_greet = refuse_out_of_scope(state_greeting)
    assert "Hello! How can I help you with AWS today?" in res_greet["generation"]

    # Thank you pleasantry
    state_thanks: AgentState = {"messages": [HumanMessage(content="thank you very much")], "classification": "conversational"}
    res_thanks = refuse_out_of_scope(state_thanks)
    assert "You're welcome! Let me know if you have any questions about AWS." in res_thanks["generation"]

    # Goodbye pleasantry
    state_bye: AgentState = {"messages": [HumanMessage(content="Goodbye for now")], "classification": "conversational"}
    res_bye = refuse_out_of_scope(state_bye)
    assert "Goodbye! Feel free to reach out" in res_bye["generation"]

def test_route_domain():
    state_aws: AgentState = {"is_aws_related": True}
    state_non_aws: AgentState = {"is_aws_related": False}
    
    assert route_domain(state_aws) == "rewrite_query"
    assert route_domain(state_non_aws) == "refuse_out_of_scope"

def test_route_history():
    state_no_history: AgentState = {"standalone_query": "How to create an S3 bucket?"}
    state_with_history: AgentState = {"standalone_query": "What did we talk about in the last session?"}
    
    assert route_history(state_no_history) == "retrieve_local"
    assert route_history(state_with_history) == "fetch_session_summary"

def test_route_search():
    state_search_needed: AgentState = {"search_needed": True}
    state_no_search: AgentState = {"search_needed": False}
    
    assert route_search(state_search_needed) == "live_aws_search"
    assert route_search(state_no_search) == "generate_answer"

@patch("backend.app.agents.nodes.classify.ChatBedrock")
def test_classify_node_aws(mock_bedrock):
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = AIMessage(content='{"is_aws_related": true}')
    mock_bedrock.return_value = mock_llm
    
    state: AgentState = {"messages": [HumanMessage(content="Explain VPC peering")]}
    res = classify_domain(state)
    
    assert res["is_aws_related"] is True
    assert res["loop_count"] == 0
