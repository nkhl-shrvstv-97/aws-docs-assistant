#!/usr/bin/env python3
import sys
import uuid
import requests

BACKEND_URL = "http://localhost:8000/api"

def main():
    print("====================================================")
    print("       AWS Documentation Agentic Chatbot CLI        ")
    print("====================================================")
    print("Type your question and press Enter.")
    print("Type 'exit' or 'quit' to save conversation summary and end.")
    print("----------------------------------------------------\n")
    
    thread_id = str(uuid.uuid4())
    print(f"[Session ID: {thread_id}]\n")
    
    while True:
        try:
            prompt = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
            
        if not prompt:
            continue
            
        if prompt.lower() in ["exit", "quit"]:
            print("\nEnding session and summarizing...")
            try:
                resp = requests.post(f"{BACKEND_URL}/end-session", json={"thread_id": thread_id}, timeout=30)
                if resp.status_code == 200:
                    data = resp.json()
                    print(f"Success: {data.get('message')}")
                    if data.get("summary"):
                        print(f"Session Summary: {data.get('summary')}")
                else:
                    print(f"Error ending session: {resp.status_code} - {resp.text}")
            except Exception as e:
                print(f"Could not reach backend to end session: {e}")
            print("Goodbye!")
            break
            
        # Send prompt to chat endpoint
        try:
            resp = requests.post(
                f"{BACKEND_URL}/chat",
                json={"prompt": prompt, "thread_id": thread_id},
                timeout=60
            )
            
            if resp.status_code == 200:
                data = resp.json()
                print(f"\nAssistant: {data.get('response')}\n")
                
                # Print sources if available
                sources = data.get("sources", [])
                if sources:
                    print("Sources:")
                    for idx, src in enumerate(sources):
                        print(f"  [{idx+1}] {src.get('title')} - {src.get('url')}")
                    print()
            else:
                print(f"\n[Error: {resp.status_code} - {resp.text}]\n")
        except Exception as e:
            print(f"\n[Error connecting to backend: {e}]\n")

if __name__ == "__main__":
    main()
