from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

TEST_CASES = [
    {
        "session_id": "eval_001",
        "question": "What is the status of my order NK0002?",
        "expected_status": 200,
        "expected_text": "Shipped",
    },
    {
        "session_id": "eval_002",
        "question": "How long does a COD refund take for order NK0002?",
        "expected_status": 200,
        "expected_text": "5 to 7 business days",
    },
    {
        "session_id": "eval_003",
        "question": "What is the status of my order?",
        "expected_status": 400,
        "expected_text": "Please provide your order ID",
    },

{
    "session_id": "eval_004",
    "question": "What is the status of my order NK0001?",
    "expected_status": 200,
    "expected_text": "Placed",
},
{
    "session_id": "eval_005",
    "question": "What is the status of my order NK0002?",
    "expected_status": 200,
    "expected_text": "NK0002",
},
{
    "session_id": "eval_006",
    "question": "Can you check my order without an order ID?",
    "expected_status": 400,
    "expected_text": "Please provide your order ID",
},
{
        "session_id": "eval_007",
        "question": "Is my order NK0001 delayed?",
        "expected_status": 200,
        "expected_text": "delayed",
    },
{
        "session_id": "eval_008",
        "question": "What is the status of order NK0002?",
        "expected_status": 200,
        "expected_text": "Shipped",
    },
{
        "session_id": "eval_009",
        "question": "How long does a cash on delivery refund take for order NK0002?",
        "expected_status": 200,
        "expected_text": "5 to 7 business days",
    },
        {
        "session_id": "eval_010",
        "question": "What is the status of order nk0002?",
        "expected_status": 200,
        "expected_text": "NK0002",
    },
    {
        "session_id": "eval_011",
        "question": "Please check my order.",
        "expected_status": 400,
        "expected_text": "Please provide your order ID",
    },
    {
        "session_id": "eval_012",
        "question": "Can you tell me the status of NK0001?",
        "expected_status": 200,
        "expected_text": "Placed",
    },
        {
        "session_id": "eval_memory_013",
        "question": "What is the status of order NK0002?",
        "expected_status": 200,
        "expected_text": "Shipped",
    },
    {
        "session_id": "eval_memory_013",
        "question": "What is my order ID?",
        "expected_status": 200,
        "expected_text": "NK0002",
    },
    {
        "session_id": "eval_memory_013",
        "question": "How long will my COD refund take?",
        "expected_status": 200,
        "expected_text": "5 to 7 business days",
    },
]
total_tests = len(TEST_CASES)
passed_tests = 0
for case in TEST_CASES:
    response = client.post(
        "/chat",
        json={
            "session_id": case["session_id"],
            "question": case["question"],
        },
    )

    response_text = response.text

    if case["session_id"] == "eval_004":
        print("DEBUG eval_004 HTTP:", response.status_code)
        print("DEBUG eval_004 RESPONSE:", response.text)

    passed = (
        response.status_code == case["expected_status"]
        and case["expected_text"].lower() in response_text.lower()
    )
    if passed:
        passed_tests += 1

    print(
        f"{case['session_id']}: "
        f"{'PASS' if passed else 'FAIL'} "
        f"(HTTP {response.status_code})"
    )

failed_tests = total_tests - passed_tests
pass_rate = (passed_tests / total_tests * 100) if total_tests else 0

print("\n===== EVALUATION SUMMARY =====")
print(f"Total Tests: {total_tests}")
print(f"Passed: {passed_tests}")
print(f"Failed: {failed_tests}")
print(f"Pass Rate: {pass_rate:.2f}%")