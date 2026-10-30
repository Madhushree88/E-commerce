from functools import lru_cache


@lru_cache(maxsize=100)
def get_cached_policy(policy_name: str) -> str:
    """
    Retrieve a fictional policy for the academic simulation.
    Repeated requests for the same policy use the cache.
    """

    policies = {
        "cod_refunds": (
            "COD refunds are processed through bank transfer "
            "after the returned item passes quality inspection. "
            "The stated timeframe is 5–7 business days "
            "after approval."
        ),
        "delivery_sla": (
            "Delivery timelines depend on the shipping method "
            "and destination. Refer to the simulated policy "
            "documents for specific details."
        ),
    }

    return policies.get(
        policy_name,
        "Policy not found. Please escalate to support."
    )