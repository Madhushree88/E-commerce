import re
from crewai_agents import run_support_agent
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
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

       
    except ValueError as e:
        print("DEBUG CHAT ERROR:", str(e))
        raise HTTPException(
            status_code=400,
            detail="Your request could not be processed safely. Please check the order details and try again."
        )


@app.websocket("/ws/chat")

async def websocket_chat(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()

            session_id = data.get("session_id")
            question = data.get("question")

            if not session_id or not question:
                await websocket.send_json({
                    "error": "Session ID and question are required."
                })
                continue

            order_match = re.search(
                r"\bNK\d{4}\b",
                question,
                re.IGNORECASE
            )

            remembered_order_id = get_order_id_from_memory(
                session_id
            )

            if not order_match and not remembered_order_id:
                await websocket.send_json({
                    "error": "Please provide your order ID, such as NK0002."
                })
                continue

            try:
                agent_response = run_support_agent(
                    customer_question=question,
                    session_id=session_id
                )

                await websocket.send_json({
                    "session_id": session_id,
                    "customer_question": question,
                    "agent_response": agent_response
                })

            except ValueError:
                await websocket.send_json({
                    "error": "Your request could not be processed safely."
                })

    except WebSocketDisconnect:
        print("WebSocket client disconnected.")        