import re

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from session_memory import get_order_id_from_memory
app = FastAPI(title="Nykaa Customer Support Agent API")
class ChatRequest(BaseModel):
    session_id: str
    question: str

@app.post("/chat")
def chat(request: ChatRequest):
    from crewai_agents import run_support_agent
    order_match = re.search(
            r"\bNK\d{4}\b",
            request.question,
            re.IGNORECASE
        )

    remembered_order_id = get_order_id_from_memory(
            request.session_id
        )

    if not order_match and not remembered_order_id:
            raise HTTPException(
                status_code=400,
                detail="Please provide your order ID, such as NK0002."
            )
    try:
        agent_response = run_support_agent(
            customer_question=request.question,
            session_id=request.session_id
        )

        return {
            "session_id": request.session_id,
            "customer_question": request.question,
            "agent_response": agent_response
        }

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Your request could not be processed safely. Please check the order details and try again."
        )