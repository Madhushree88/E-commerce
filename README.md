# Nykaa Domain Support Agent

## Academic Capstone Project

**Domain:** E-commerce and Retail  
**Implementation:** Python, RAG, CrewAI, AutoGen, FastAPI  
**Execution mode:** Offline simulation using mock LLM responses

## 1. Project Overview

This project demonstrates an agentic customer-support system for a fictional e-commerce environment inspired by the Nykaa retail domain.

The system is designed to answer customer policy questions, retrieve simulated order information, coordinate specialized agents, maintain conversation context, and apply safety and governance checks.

**Important disclaimer:** This is an academic simulation. The project does not use real Nykaa customer records, official company policies, or live business systems. All order records, policies, and business rules are fictional.

## 2. Project Objectives

- Build and validate a synthetic e-commerce order dataset.
- Implement retrieval-augmented generation (RAG) over a fictional policy knowledge base.
- Coordinate specialized customer-support agents using CrewAI.
- Demonstrate a separate AutoGen multi-agent review workflow.
- Expose customer-support functionality through FastAPI and WebSocket interfaces.
- Maintain conversation context using session-based memory.
- Apply PII masking, prompt-injection checks, response validation, and escalation logic.
- Evaluate the system using repeatable functional tests and audit logs.

## 3. Synthetic Dataset

The project generates 50 fictional customer orders using a fixed random seed of 42.

### Dataset Configuration

- Categories: Apparel, Electronics, Home, Footwear, Beauty
- Statuses: Placed, Shipped, Delivered, Returned, Refunded
- Order amount range: INR 300–15,000
- Order age range: 0–30 days
- Delayed shipment probability: 20%

### Validated Distribution

| Category | Orders |
|---|---:|
| Apparel | 10 |
| Electronics | 9 |
| Home | 11 |
| Footwear | 10 |
| Beauty | 10 |
| **Total** | **50** |

| Status | Orders |
|---|---:|
| Placed | 11 |
| Shipped | 11 |
| Delivered | 9 |
| Returned | 6 |
| Refunded | 13 |

Delayed shipments: 10 of 50 orders (20%).

All implemented dataset validation checks passed.

To regenerate the dataset:

```bash
python dataset.py
```

Generated file: `data/orders.json`

## 4. Knowledge Base and RAG

The project contains 12 fictional customer-support policy documents in `knowledge_base/`, covering topics such as cancellations, returns, refunds, damaged items, delivery, payments, exchanges, and escalation.

The RAG implementation includes:

- Document chunking with overlap
- Sentence-transformer embeddings
- ChromaDB vector storage
- Similarity-based retrieval
- Out-of-scope query thresholding
- Retrieval evaluation using document-level precision and recall

Relevant files include `rag_index.py`, `rag_search.py`, `rag_evaluation.py`, and `rag_threshold.py`.

The RAG component provides policy context; it does not independently authorize refunds or change order records.

## 5. CrewAI Multi-Agent Workflow

The primary support workflow coordinates three specialized responsibilities:

1. **Policy Retrieval Agent:** Retrieves relevant fictional policy information.
2. **Order Lookup Agent:** Checks the synthetic order register.
3. **Response Composer Agent:** Produces a customer-facing response based on retrieved information.

The workflow includes validation, escalation scoring, session memory, audit logging, and response safeguards.

Key implementation files include:

- `crewai_agents.py`
- `mock_llm.py`
- `policy_tool.py`
- `order_tool.py`
- `order_lookup.py`
- `escalation.py`
- `validation.py`

The system uses deterministic mock LLM behavior for offline testing. It does not require a paid LLM API key for the demonstrated workflow.

## 6. AutoGen Multi-Agent Review

A separate AutoGen workflow demonstrates collaboration between three review agents:

1. **Policy Reviewer:** Checks fictional policy information.
2. **Order Reviewer:** Checks the simulated order facts.
3. **Final Editor:** Produces a consolidated review response.

The demonstration uses `RoundRobinGroupChat` and replayed mock model responses.

A separate rule-based validation function checks selected properties of the final response, including order ID consistency, COD refund timeframe wording, and unsupported approval claims.

Relevant files:

- `autogen_workflow.py`
- `autogen_validation.py`
- `cache_manager.py`

The Final Editor output is scripted in this demonstration. The validation rules provide targeted checks, not a guarantee of complete factual or security correctness.

## 7. Session Memory and Caching

Session memory uses LangChain's in-memory chat history to support follow-up customer questions within the running application process.

The implementation can recover a previously mentioned synthetic order ID from conversation history.

Policy caching uses Python's `lru_cache` to reuse predefined fictional policy text within the AutoGen demonstration.

**Limitations:** Session history and cache entries are in memory and are not persisted across process restarts. The cached policy demonstration is not a replacement for live RAG retrieval.

## 8. API and WebSocket

The application uses FastAPI to expose the support workflow.

Implemented interfaces:

- `POST /chat` — customer-support requests
- `WebSocket /ws/chat` — WebSocket-based support interaction

The application can be started using the CrewAI virtual environment:

```bash
source .venv-crewai/bin/activate
uvicorn main:app --reload
```

The API is intended for local academic demonstration, not production deployment.

## 9. Safety and Governance

The project includes rule-based safeguards for:

- Personally identifiable information (PII) masking
- Prompt-injection detection
- Response grounding checks
- Unsupported refund-approval claims
- Order ID consistency
- Escalation decisions
- Audit logging

Relevant files include:

- `pii_masking.py`
- `prompt_guard.py`
- `response_guard.py`
- `audit_logger.py`
- `governance_report.md`

Audit records are stored locally in JSONL format.

These controls are educational demonstrations and have not undergone comprehensive security or compliance testing.

## 10. Evaluation Results

The functional evaluation suite includes 15 test scenarios covering customer-support behavior and related checks.

**Latest confirmed result:**

- Total functional tests: 15
- Passed: 15
- Failed: 0
- Pass rate: 100%

The result applies to the implemented test suite and should not be interpreted as a production accuracy guarantee.

Additional testing includes RAG evaluation, AutoGen final-response validation, and in-memory caching checks.

See `agent_evaluation.py`, `evaluation_report.md`, and `rag_evaluation.py`.

## 11. Local Development Environment

The project uses separate Python virtual environments to isolate dependencies:

| Environment | Purpose |
|---|---|
| `.venv` | RAG and embedding dependencies |
| `.venv-crewai` | CrewAI, FastAPI, and primary support workflow |
| `.venv-autogen` | AutoGen review workflow |

Virtual environments are excluded from Git and should be created locally as needed.

### Run the AutoGen Demonstration

From the project directory:

```bash
source .venv-autogen/bin/activate
python autogen_workflow.py
```

The demonstration uses replayed mock responses and does not require an external LLM API key.

### Run the Functional Evaluation

Using the CrewAI environment:

```bash
source .venv-crewai/bin/activate
python agent_evaluation.py
```

## 12. Known Limitations

- All records and policies are simulated.
- No real customer data or real refund transactions are processed.
- Mock and replayed LLM responses are used instead of live model reasoning.
- Memory and caching are process-local.
- Rule-based guardrails do not cover every possible unsafe or incorrect response.
- The demonstrated evaluation suite is limited in scope.
- The project has not been validated for production security, scalability, or reliability.

## 13. Project Deliverables

The repository contains source code, synthetic data generation, a fictional policy knowledge base, agent workflows, evaluation scripts, governance documentation, and audit logging.

This capstone demonstrates the integration of RAG, multi-agent coordination, API interfaces, memory, caching, testing, and governance principles within a controlled academic environment.