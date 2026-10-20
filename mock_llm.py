from crewai.llms.base_llm import BaseLLM
from order_tool import order_status_tool
from policy_tool import policy_search_tool

class MockLLM(BaseLLM):

    def __init__(self):
        super().__init__(model="mock-nykaa-llm")

    def supports_function_calling(self):
        return True

    def call(
        self,
        messages,
        tools=None,
        callbacks=None,
        available_functions=None,
        from_task=None,
        from_agent=None,
        response_model=None,
    ):
        agent_role = getattr(from_agent, "role", None)

        print("DEBUG - Tools received:", bool(tools))
        print("DEBUG - Current agent:", agent_role)
        if agent_role == "Nykaa Policy Retrieval Specialist":
            import re

            message_text = str(messages)

            question_match = re.search(
                r"Respond to this customer question:\s*'([^']+)'",
                message_text
            )

            if not question_match:
                return "Customer question not found. Please escalate to support."

            customer_question = question_match.group(1)

            print("DEBUG - Customer question:", customer_question)
            print("DEBUG - Searching policy documents")

            result = policy_search_tool.run(
                question=customer_question
            )

            return str(result)
        if agent_role == "Nykaa Customer Response Composer":
            import re

            message_text = str(messages)

            order_match = re.search(
                r"Order ID:\s*(NK\d+)",
                message_text
            )

            status_match = re.search(
                r"Status:\s*(\w+)",
                message_text
            )

            delay_match = re.search(
                r"Delayed Shipment:\s*(True|False)",
                message_text
            )

            if not all([order_match, status_match, delay_match]):
                return (
                    "Dear Customer,\n\n"
                    "We could not verify your order details. "
                    "Please contact our support team.\n\n"
                    "Nykaa Customer Support"
                )

            order_id = order_match.group(1)
            status = status_match.group(1)
            delayed = delay_match.group(1) == "True"

            response = (
                f"Dear Customer,\n\n"
                f"Your order {order_id} is currently marked as "
                f"{status}. "
            )

            if delayed:
                response += (
                    "Our records indicate that your shipment is delayed. "
                    "We apologize for the inconvenience. "
                    "Our support team should review the delay and "
                    "provide an updated delivery estimate."
                )
            else:
                response += (
                    "Our records do not currently indicate "
                    "a delayed shipment."
                )
            if (
                "Source: cod_refunds.md" in message_text
                and "5 to 7 business days" in message_text
            ):
                response += (
                    "\n\nRegarding your COD refund question: "
                    "According to our support policy, COD refunds "
                    "are processed by bank transfer after the returned "
                    "item passes quality inspection. Once approved, "
                    "the refund normally reaches the customer's bank "
                    "account within 5 to 7 business days. "
                    "This does not confirm refund eligibility "
                    "for your particular order."
                )
            priority_match = re.search(
                r"Escalation Priority:\s*(High|Medium|Low)",
                message_text
            )

            if priority_match and priority_match.group(1) == "High":
                response += (
                    "\n\nYour order has been identified as "
                    "high priority based on the shipment delay "
                    "and order age. We recommend escalating "
                    "this case to a human support agent "
                    "for further review."
                )
            response += (
                "\n\nThank you for your patience.\n"
                "Nykaa Customer Support"
            )

            return response
        if tools:
            print("DEBUG - Executing order lookup tool")
            result = order_status_tool.run(record_id="NK0001")
            return str(result)

        return (
            "This is a simulated response from the Nykaa "
            "customer support assistant."
        )