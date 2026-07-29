from backend.app.agents.state import AgentState

def refuse_out_of_scope(state: AgentState) -> dict:
    """
    Sets a static refusal response.
    """
    print("--- NODE: REFUSE OUT OF SCOPE ---")
    refusal = "I'm sorry, I am an AI assistant dedicated to helping with AWS Documentation. I can only assist with AWS-related services, architectures, pricing, or concepts."
    return {"generation": refusal}
