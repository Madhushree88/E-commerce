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
    return {
        "session_id": request.session_id,
        "customer_question": request.question,
        "message": "Customer question received successfully"
    }