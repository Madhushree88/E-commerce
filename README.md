
# Nykaa Domain Support Agent

## Capstone Track
Nykaa (E-commerce & Retail)

## Project Overview
This project develops a customer-support agent using
RAG, CrewAI, AutoGen, and FastAPI.

The agent will answer policy questions, retrieve
fictional order records, and apply safety guardrails.

## Part 1 — Dataset Design

### Dataset Configuration
- Random seed: 42
- Total records: 50
- Categories: Apparel, Electronics, Home,
  Footwear, Beauty
- Statuses: Placed, Shipped, Delivered,
  Returned, Refunded
- Order amount range: INR 300–15,000
- Order age: 0–30 days
- Delayed shipment probability: 20%

### Generation Method
The generator guarantees at least three records
per category, then randomly assigns categories
to the remaining records.

Statuses are randomly selected, with the first
five records assigned the five required statuses
to guarantee coverage.

All five categories and statuses have equal
selection probability during random generation.

Shipment delays are assigned using a 20%
Bernoulli probability with a fixed random seed.

### Price Range Justification
INR 300–15,000 is an illustrative range chosen
to cover inexpensive beauty and apparel items
through higher-value electronics and home products.

### Validation Results
- Total records: 50
- Apparel: 10
- Electronics: 9
- Home: 11
- Footwear: 10
- Beauty: 10
- Placed: 11
- Shipped: 11
- Delivered: 9
- Returned: 6
- Refunded: 13
- Delayed shipments: 10/50 (20%)

All implemented dataset validation checks passed.

### Reproduce the Dataset
Run:

    python dataset.py

Generated output:

    data/orders.json

## Development Mode
The completed project will support deterministic
MOCK_LLM execution without API keys.

## Project Status
Part 1, Task 1: Dataset generation and validation complete.
Remaining tasks: In progress.
