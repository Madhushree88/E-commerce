from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

with client.websocket_connect("/ws/chat") as websocket:
    websocket.send_json({
        "session_id": "ws_memory_test_001",
        "question": "What is the status of my order NK0002?"
    })

    first_response = websocket.receive_json()
    print("FIRST RESPONSE:")
    print(first_response)

    websocket.send_json({
        "session_id": "ws_memory_test_001",
        "question": "How long does a Cash on Delivery refund take for my order?"
    })

    second_response = websocket.receive_json()
    print("\nSECOND RESPONSE:")
    print(second_response)