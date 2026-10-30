
import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_ext.models.replay import ReplayChatCompletionClient
from autogen_validation import validate_final_response


# 1. Mock model clients

policy_mock_client = ReplayChatCompletionClient(
    chat_completions=[
        "According to the simulated COD refund policy, "
        "refunds are processed through bank transfer after "
        "the returned item passes quality inspection. "
        "The stated timeframe is 5–7 business days after approval. "
        "This does not confirm approval for any specific order."
    ]
)

order_mock_client = ReplayChatCompletionClient(
    chat_completions=[
        "Simulated order NK0002 has status Shipped. "
        "The order amount is INR 4312, and the shipment "
        "is not marked as delayed. "
        "These details come from the fictional test dataset. "
        "No refund approval has been confirmed."
    ]
)

editor_mock_client = ReplayChatCompletionClient(
    chat_completions=[
        "FINAL EDITOR VERDICT: APPROVED FOR SIMULATED RESPONSE. "
        "Order NK0002 is Shipped and is not marked as delayed. "
        "Under the fictional COD refund policy, refunds are "
        "processed by bank transfer after return quality inspection, "
        "with a stated timeframe of 5–7 business days after approval. "
        "No refund has been approved or initiated. "
        "This information is from an academic simulation."
    ]
)


# 2. Define agents

policy_reviewer = AssistantAgent(
    name="Policy_Reviewer",
    system_message=(
        "You are a policy reviewer for a simulated e-commerce "
        "customer support system. "
        "Review customer questions against the fictional policies "
        "provided in the task. "
        "Do not invent policies, refund approvals, or timelines. "
        "If policy information is missing, clearly say so. "
        "Do not claim to access real Nykaa systems or data."
    ),
    model_client=policy_mock_client,
)

order_reviewer = AssistantAgent(
    name="Order_Reviewer",
    system_message=(
        "You are an order reviewer for a simulated e-commerce "
        "customer support system. "
        "Review the fictional order information provided in the task. "
        "Check order status, shipment delays, and relevant order details. "
        "Do not invent order records, delivery dates, or refund approvals. "
        "If order information is missing, clearly say so. "
        "Do not claim to access real Nykaa systems or customer data."
    ),
    model_client=order_mock_client,
)

final_editor = AssistantAgent(
    name="Final_Editor",
    system_message=(
        "You are the Final Editor for a simulated e-commerce "
        "customer support multi-agent system. "
        "Review the findings from the Policy Reviewer and "
        "Order Reviewer. "
        "Check that the response is consistent with the fictional "
        "policy and simulated order details. "
        "Do not approve unsupported refund claims or invent facts. "
        "Clearly distinguish policy information from confirmed "
        "actions on a customer's order. "
        "Provide a final verdict and a safe customer-facing response."
    ),
    model_client=editor_mock_client,
)


# 3. Create group conversation

review_team = RoundRobinGroupChat(
    participants=[
        policy_reviewer,
        order_reviewer,
        final_editor,
    ],
    termination_condition=MaxMessageTermination(
        max_messages=4
    ),
)


# 4. Run workflow

async def main():
    result = await review_team.run(
        task=(
            "Review simulated order NK0002 and explain the "
            "fictional COD refund policy. "
            "Do not claim that any refund has been approved."
        )
    )

    final_response = None

    for message in result.messages:
        print(f"\n--- {message.source} ---")
        print(message.content)

        if message.source == "Final_Editor":
            final_response = message.content

    print("\n--- RULE-BASED VALIDATION ---")

    if final_response is None:
        print("REJECTED: Final Editor response is missing.")
    else:
        validation = validate_final_response(
            final_response,
            expected_order_id="NK0002",
        )

        print("Verdict:", validation["verdict"])
        print("Issues:", validation["issues"])

        if validation["valid"]:
            print("Final response passed the configured validation checks.")
        else:
            print("Final response rejected. Human review required.")


if __name__ == "__main__":
    asyncio.run(main())
