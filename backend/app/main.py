import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from backend.app.routers import chat

from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from backend.app.routers.chat import limiter

app = FastAPI(
    title="AWS Documentation Agentic Chatbot",
    description="FastAPI backend hosting LangGraph RAG Agent for AWS Documentation",
    version="1.0.0"
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Enable CORS for frontend/testing calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(chat.router, prefix="/api", tags=["chat"])

from backend.app.db.init_db import init_database

@app.on_event("startup")
def on_startup():
    init_database()

@app.get("/", response_class=HTMLResponse)
def read_root():
    static_file_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(static_file_path):
        with open(static_file_path, "r") as f:
            return f.read()
    return "<h3>AWS Docs Assistant Chat Interface not found.</h3>"

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)

