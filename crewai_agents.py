from audit_logger import write_audit_log
from policy_tool import policy_search_tool
from pii_masking import mask_pii
import os
from prompt_guard import detect_prompt_injection
from response_guard import check_response_guardrail, check_order_grounding

os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["MOCK_LLM"] = "true"

from crewai import Agent, Task, Crew, Process
from mock_llm import MockLLM
from order_tool import order_status_tool
mock_llm = MockLLM()
retrieval_agent = Agent(
    role="Nykaa Policy Retrieval Specialist",
    goal="Find relevant policy information for customer questions.",
    backstory=(
        "You are a customer support policy specialist "
        "working with fictional Nykaa policy documents."
    ),
    tools=[policy_search_tool],
    llm=mock_llm,
    verbose=False,
    allow_delegation=False,
    )
order_lookup_agent = Agent(
    role="Nykaa Order Lookup Specialist",
    goal="Check customer order details accurately.",
    backstory=(
        "You are a customer support specialist responsible "
        "for checking simulated Nykaa order records."
    ),
    tools=[order_status_tool],
    llm=mock_llm,
    verbose=False,
    allow_delegation=False,
)

print("Order Lookup Agent created successfully!")
print("Order Lookup Agent role:", order_lookup_agent.role)
print("\n--- Order Lookup Agent Tools ---")

for agent_tool in order_lookup_agent.tools:
    print("Registered tool:", agent_tool.name)
response_composer_agent = Agent(
    role="Nykaa Customer Response Composer",
    goal=(
        "Prepare clear, polite, and accurate customer support "
        "responses using verified order details and policy information."
    ),
    backstory=(
        "You are a customer support communication specialist. "
        "You explain fictional Nykaa policies in simple language "
        "and never invent order information or refund promises."
    ),
    llm=mock_llm,
    verbose=False,
    allow_delegation=False,
)

print("Response Composer Agent created successfully!")
print("Response Composer role:", response_composer_agent.role)
print("Retrieval Agent created successfully!")
print("Agent role:", retrieval_agent.role)
print("Agent goal:", retrieval_agent.goal)
customer_question = "How long does a Cash on Delivery refund take?"
if detect_prompt_injection(customer_question):
    raise ValueError("Suspicious customer instruction detected.")
retrieval_task = Task(
    description=(
        f"Respond to this customer question: "
        f"'{customer_question}' "
        "This is an initial mock test only."
    ),
    expected_output="A short simulated customer support response.",
    agent=retrieval_agent,
)
order_lookup_task = Task(
    description=(
        "Check the simulated Nykaa order with record ID NK0001. "
        "Use the Check Order Status tool to retrieve the order details. "
        "Do not invent any order information."
    ),
    expected_output=(
        "The order ID, category, status, order value, "
        "days since creation, and delayed shipment status."
    ),
    agent=order_lookup_agent,
)
response_composer_task = Task(
    description=(
        "Prepare a clear, polite customer support response "
        "using the policy information and order details "
        "from the previous two tasks. "
        "Do not invent order details or policy rules."
    ),
    expected_output=(
        "A customer-friendly response explaining the order "
        "status and relevant policy information."
    ),
    agent=response_composer_agent,
    context=[retrieval_task, order_lookup_task],
)
crew = Crew(
    agents=[
        retrieval_agent,
        order_lookup_agent,
        response_composer_agent
    ],
    tasks=[
    retrieval_task,
    order_lookup_task,
    response_composer_task
],
    process=Process.sequential,
    memory=False,
    verbose=False,
)


print("\nStarting first CrewAI task...")

result = crew.kickoff()
guardrail_result = check_response_guardrail(str(result))

if not guardrail_result["passed"]:
    raise ValueError(
        "Customer response blocked: " + guardrail_result["reason"]
    )
order_grounding_result = check_order_grounding(str(result), "NK0001")

if not order_grounding_result["passed"]:
    raise ValueError(
        "Order grounding failed: " + order_grounding_result["reason"]
    )

print("Order grounding:", order_grounding_result["reason"])

print("Response guardrail:", guardrail_result["reason"])
print("\nCrewAI task result:")
print(mask_pii(str(result)))
print("\n--- Individual Task Results ---")

for index, task_output in enumerate(result.tasks_output, start=1):
    print(f"\nTask {index}")
    print("Agent:", task_output.agent)
    print("Output:", mask_pii(task_output.raw))
    write_audit_log(task_output.agent, task_output.raw)