from backend.app.agents.state import AgentState

def refuse_out_of_scope(state: AgentState) -> dict:
    """
    Sets a static refusal or conversational response.
    """
    print("--- NODE: REFUSE OUT OF SCOPE / GREET USER ---")
    classification = state.get("classification", "out_of_scope")
    
    if classification == "conversational":
        messages = state.get("messages", [])
        last_msg = messages[-1].content.strip().lower() if messages else "hello"
        
        # Simple rule-based pleasantries responder
        if any(w in last_msg for w in ["thank", "tanks", "thx", "appreciate"]):
            response_text = "You're welcome! Let me know if you have any questions about AWS."
        elif any(w in last_msg for w in ["bye", "goodbye", "see ya", "exit"]):
            response_text = "Goodbye! Feel free to reach out if you need help with AWS in the future."
        else:
            response_text = "Hello! How can I help you with AWS today?"
    else:
        response_text = "I'm sorry, I am an AI assistant dedicated to helping with AWS Documentation. I can only assist with AWS-related services, architectures, pricing, or concepts."
        
    return {"generation": response_text}
