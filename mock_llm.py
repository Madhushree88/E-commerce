
import re

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
        message_text = str(messages)

        print("DEBUG - Tools received:", bool(tools))
        print("DEBUG - Current agent:", agent_role)

        # Agent 1: Policy Retrieval Specialist
        if agent_role == "Nykaa Policy Retrieval Specialist":

            question_matches = re.findall(
                r"Respond to this customer question:\s*'([^']+)'",
                message_text
            )

            if not question_matches:
                return (
                    "Customer question not found. "
                    "Please escalate to support."
                )

            customer_question = question_matches[-1]

            print("DEBUG - Customer question:", customer_question)
            print("DEBUG - Searching policy documents")

            result = policy_search_tool.run(
                question=customer_question
            )

            return str(result)

        # Agent 3: Customer Response Composer
        if agent_role == "Nykaa Customer Response Composer":

            question_matches = re.findall(
                r"Current customer question:\s*([^\n]+)",
                message_text
            )

            customer_question = (
                question_matches[-1].strip()
                if question_matches
                else ""
            )

            order_matches = re.findall(
                r"Order ID:\s*(NK\d+)",
                message_text
            )

            status_matches = re.findall(
                r"Status:\s*(\w+)",
                message_text
            )

            delay_matches = re.findall(
                r"Delayed Shipment:\s*(True|False)",
                message_text
            )

            order_match = (
                order_matches[-1] if order_matches else None
            )
            status_match = (
                status_matches[-1] if status_matches else None
            )
            delay_match = (
                delay_matches[-1] if delay_matches else None
            )

            if not all([order_match, status_match, delay_match]):
                return (
                    "Dear Customer,\n\n"
                    "We could not verify your order details. "
                    "Please contact our support team.\n\n"
                    "Nykaa Customer Support"
                )

            order_id = order_match
            status = status_match
            delayed = delay_match == "True"

            response = (
                "Dear Customer,\n\n"
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

            # Include refund details only when the customer
            # has asked about refunds and the policy was retrieved.
            is_refund_question = bool(
                re.search(
                    r"\b(refunds?|cod|cash on delivery)\b",
                    customer_question,
                    re.IGNORECASE
                )
            )

            has_cod_policy = (
                "Source: cod_refunds.md" in message_text
                and "5 to 7 business days" in message_text
            )

            if is_refund_question and has_cod_policy:
                response += (
                    "\n\nRegarding your COD refund question: "
                    "According to our simulated support policy, "
                    "COD refunds are processed by bank transfer "
                    "after the returned item passes quality inspection. "
                    "Once approved, the refund normally reaches "
                    "the customer's bank account within "
                    "5 to 7 business days. "
                    "This does not confirm refund eligibility "
                    "or approval for your particular order."
                )

            priority_match = re.search(
                r"Escalation Priority:\s*(High|Medium|Low)",
                message_text
            )

            if (
                priority_match
                and priority_match.group(1) == "High"
            ):
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

        # Agent 2: Order Lookup Specialist
        if tools:
            print("DEBUG - Executing order lookup tool")
            print("DEBUG LOOKUP MESSAGE:", message_text[-1200:])

            order_matches = re.findall(
                r"Current Task:.*?Current customer question:"
                r"\s*(.*?)(?=\s+Use the Check Order Status tool)",
                message_text,
                re.IGNORECASE | re.DOTALL
            )

            current_question = (
                order_matches[-1] if order_matches else ""
            )

            order_match = re.search(
                r"\bNK\d{4}\b",
                current_question,
                re.IGNORECASE
            )

            if not order_match:
                order_match = re.search(
                    r"Previously verified order reference:"
                    r"\s*(NK\d{4})",
                    message_text,
                    re.IGNORECASE
                )

            print(
                "DEBUG - Order ID match found:",
                bool(order_match)
            )

            if not order_match:
                return "Order lookup requires a valid order ID."

            record_id = (
                order_match.group(1)
                if order_match.lastindex
                else order_match.group(0)
            ).upper()

            print(
                "DEBUG - Order ID passed to lookup:",
                record_id
            )

            result = order_status_tool.run(
                record_id=record_id
            )

            return str(result)

        return (
            "This is a simulated response from the Nykaa "
            "customer support assistant."
        )
