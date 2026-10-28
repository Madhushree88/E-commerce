# AI Governance and Safety Report
## Simulated Nykaa Customer Support Multi-Agent System

### 1. Introduction

This report documents the governance and safety mechanisms implemented in an academic prototype of a multi-agent e-commerce customer-support system.

The project uses synthetic order records, fictional customer-support policies, CrewAI agents, Retrieval-Augmented Generation (RAG), and a mock language model.

**Disclaimer:** This project is an independent academic simulation. It is not affiliated with Nykaa and does not use actual Nykaa customer information, official policies, or production systems.

### 2. Governance Objectives

The governance framework aims to:

1. Reduce exposure of personally identifiable information (PII).
2. Detect predefined prompt-injection attempts.
3. Prevent selected unsupported refund promises.
4. Verify that responses reference the intended order.
5. Validate COD refund timeframes against the simulated policy.
6. Prioritize potentially problematic orders for escalation.
7. Maintain an auditable record of agent outputs.

### 3. PII Protection

**Implementation:** `pii_masking.py`

The system uses regular expressions to replace recognized email addresses and Indian mobile numbers with masking tokens.

- Email addresses: `[EMAIL_MASKED]`
- Mobile numbers: `[PHONE_MASKED]`

**Verification:** A fictional email address and mobile number were both successfully masked.

**Result:** PASS

**Limitations:** The implementation does not comprehensively detect postal addresses, customer names, financial account information, or every international telephone-number format. Masking is applied only where the function is explicitly invoked.

### 4. Prompt-Injection Detection

**Implementation:** `prompt_guard.py`

The system checks text against predefined suspicious-instruction patterns, including requests to ignore prior instructions, reveal system prompts, override safety rules, or bypass security checks.

Matching is case-insensitive.

**Verification:** Three suspicious instructions were correctly detected, while one legitimate order-status question was not flagged.

**Result:** 4/4 PASS

**Limitations:** Pattern matching cannot reliably detect every prompt-injection technique, including indirect, obfuscated, multilingual, or context-dependent attacks.

### 5. Response Validation and Grounding

**Implementation:** `response_guard.py`

Three validation functions were reviewed:

- `check_response_guardrail()` detects selected unsupported refund promises.
- `check_order_grounding()` checks whether the response includes the expected order ID without mentioning another order ID.
- `check_cod_refund_grounding()` checks the fictional COD refund timeframe of 5–7 business days.

**Verification:** Six checks covered acceptable responses and responses that should be rejected.

**Result:** 6/6 PASS

**Limitations:** These functions use predefined rules and textual matching. They cannot establish complete factual correctness, detect every unsupported claim, or independently verify actual refund eligibility. Order-ID matching alone does not prove that all other order details are correct.

### 6. Escalation and Risk Prioritization

**Implementation:** `escalation.py`

The escalation score is calculated from shipment delay and order age.

| Factor | Contribution |
|---|---:|
| Delayed shipment | 70 points |
| Order age | Up to 30 points |
| Maximum total | 100 points |

Priority thresholds are:

- High: 70 points or above
- Medium: 40 to below 70 points
- Low: Below 40 points

**Verification results:**

| Simulated order | Result |
|---|---|
| NK0001 | Score 93; High priority |
| NK9999 | Order not found |

**Result:** 2/2 PASS

**Identified design limitation:** The current scoring formula cannot produce Medium priority. Non-delayed orders score at most 30, while delayed orders score at least 70. The scoring design requires refinement if all three priority categories must be operational.

A calculated priority should not be treated as proof that a human escalation or resolution has occurred.

### 7. Audit Logging

**Implementation:** `audit_logger.py`

The system records agent activity in `logs/agent_traces.jsonl`.

Each log entry contains:

- A UTC timestamp.
- The agent name.
- Agent output processed through the PII-masking function.

**Verification:** A fictional test entry was successfully written and read as JSON. Its email address and mobile number were masked.

**Result:** PASS

**Limitations:** The current implementation does not establish tamper resistance, role-based access controls, log-retention policies, comprehensive PII redaction, or secure centralized storage.

### 8. Governance Verification Summary

| Component | Tests performed | Result |
|---|---|---|
| PII masking | Fictional email and phone | PASS |
| Prompt-injection detection | 4 cases | 4/4 PASS |
| Response validation | 6 cases | 6/6 PASS |
| Escalation | 2 cases | 2/2 PASS |
| Audit logging | One fictional log entry | PASS |

All five reviewed governance components passed their initial targeted checks.

These checks are separate from the project's 15 functional API evaluation cases, which also passed.

### 9. Recommended Improvements

Before considering deployment beyond an academic prototype, the following improvements are recommended:

1. Expand PII detection and define secure data-handling and retention policies.
2. Introduce stronger defenses against indirect and obfuscated prompt injection.
3. Validate response claims against structured order and policy evidence.
4. Revise escalation scoring so that the intended priority categories are reachable.
5. Establish explicit human-review requirements for sensitive refund and exception decisions.
6. Add structured audit event identifiers, access controls, and tamper-evident storage.
7. Expand evaluation to cover adversarial inputs, concurrency, session isolation, and failure recovery.

### 10. Conclusion

The simulated Nykaa Customer Support Multi-Agent System includes foundational governance mechanisms for PII masking, prompt-injection detection, response grounding, escalation prioritization, and audit logging.

All five reviewed components passed their initial targeted tests. Together with the 15 passing functional evaluation cases, these results demonstrate progress toward a traceable and controlled academic prototype.

However, successful targeted tests do not establish comprehensive security, regulatory compliance, or production readiness. Further design improvements and broader testing are required before real-world use.