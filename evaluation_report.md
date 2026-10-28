# Evaluation Report: Nykaa Customer Support Multi-Agent System

## 1. Project Overview

This capstone project develops a prototype multi-agent customer support system for a simulated Nykaa-style e-commerce environment.

The system combines Retrieval-Augmented Generation (RAG), CrewAI agent orchestration, order-status lookup, conversation memory, FastAPI endpoints, and rule-based validation.

**Important disclaimer:** This is an independent academic simulation. The project does not use actual Nykaa customer records, official company policies, or live business systems.

## 2. Evaluation Objectives

The evaluation aims to verify whether the prototype can:

1. Retrieve and communicate simulated order information accurately.
2. Respond to customer questions using the fictional policy knowledge base.
3. Handle delayed-shipment and cash-on-delivery refund questions.
4. Reject requests without an available order reference.
5. Recognize lowercase order IDs.
6. Retain an order reference across multiple messages within the same session.

## 3. Evaluation Methodology

The evaluation uses 15 predefined functional test cases executed through the FastAPI `/chat` endpoint using a Python test client.

Each test specifies:

- A customer question.
- A session identifier.
- An expected HTTP response status.
- A required text fragment in the response.

A test passes only when both the HTTP status and expected response text match.

The final three tests share a session identifier to evaluate conversation-memory continuity.

The tests run against synthetic order records, fictional support policies, and a mock language model. They are not live customer-service evaluations.

## 4. Evaluation Results

| Metric | Result |
|---|---:|
| Total test cases | 15 |
| Passed | 15 |
| Failed | 0 |
| Functional test pass rate | 100.00% |

The final execution of `agent_evaluation.py` reported all 15 tests passing.

The test cases cover order status, delayed shipments, COD refund timing, missing order references, case-insensitive order IDs, and multi-turn memory.

## 5. Key Findings

**Order lookup:** The prototype successfully returned expected information for the simulated orders tested.

**Policy responses:** The tested COD refund questions returned the expected fictional policy timeframe.

**Input validation:** Requests lacking an order ID and without a previously remembered order reference returned HTTP 400.

**Conversation memory:** Three sequential requests sharing the same session ID passed, including follow-up questions without repeating the order ID.

**Grounding correction:** During development, an order-ID extraction defect was identified and corrected. Subsequent evaluation confirmed that the tested follow-up requests used the intended order reference.

## 6. Limitations

The evaluation has several important limitations:

- The dataset contains only 50 synthetic orders.
- The knowledge base contains 12 fictional policy documents.
- The test suite contains 15 predefined cases, rather than a statistically representative sample.
- The mock LLM does not demonstrate the behavior of a deployed generative model.
- Expected-text matching cannot fully assess semantic correctness, factual completeness, helpfulness, or customer satisfaction.
- Performance, concurrent-user behavior, and production-scale reliability have not been established by this test suite.
- The 15 tests do not provide comprehensive evidence of prompt-injection resistance, PII protection, escalation correctness, or WebSocket reliability.

## 7. Conclusion

The prototype achieved a **100.00% pass rate across 15 predefined functional tests**, demonstrating successful execution of the tested customer-support workflows in the simulated environment.

The results support the feasibility of the prototype for academic demonstration. Further evaluation is required before making claims about security, scalability, production reliability, or real-world customer-service effectiveness.