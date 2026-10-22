from fastapi import FastAPI

app = FastAPI(title="Nykaa Customer Support Agent API")


@app.get("/")
def home():
    return {
        "message": "Nykaa Customer Support API is running",
        "status": "success"
    }
from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    question: str


@app.post("/chat")
def chat(request: ChatRequest):
    from crewai_agents import run_support_agent

    agent_response = run_support_agent(
        customer_question=request.question,
        session_id=request.session_id
    )

    return {
        "session_id": request.session_id,
        "customer_question": request.question,
        "agent_response": agent_response
    }