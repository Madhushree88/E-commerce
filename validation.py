from typing import Literal
from pydantic import BaseModel, Field


class EscalationResult(BaseModel):
    record_id: str
    escalation_score: float = Field(ge=0, le=100)
    priority: Literal["Low", "Medium", "High"]
    delayed_shipment: bool
    days_since_created: int = Field(ge=0)