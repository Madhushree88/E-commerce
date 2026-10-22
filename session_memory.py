from langchain_core.chat_history import InMemoryChatMessageHistory

sessions = {}


def get_session_history(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = InMemoryChatMessageHistory()

    return sessions[session_id]


def add_customer_message(session_id: str, message: str):
    history = get_session_history(session_id)
    history.add_user_message(message)


def add_agent_message(session_id: str, message: str):
    history = get_session_history(session_id)
    history.add_ai_message(message)


def reset_session(session_id: str):
    sessions.pop(session_id, None)
def get_conversation_context(session_id: str) -> str:
    history = get_session_history(session_id)
    if not history.messages:
        return "No previous conversation."

    conversation = []

    for message in history.messages:
        if message.type == "human":
            role = "Customer"
        else:
            role = "Support Agent"

        conversation.append(f"{role}: {message.content}")

    return "\n".join(conversation)
def get_order_id_from_memory(session_id: str):
    import re

    history = get_session_history(session_id)

    for message in reversed(history.messages):
        if message.type == "human":
            match = re.search(
                r"\bNK\d{4}\b",
                message.content,
                re.IGNORECASE
            )

            if match:
                return match.group(0).upper()

    return None