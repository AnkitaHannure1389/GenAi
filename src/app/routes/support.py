from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from src.app.llm_client import LLMClient

router = APIRouter(prefix="/support", tags=["support"])


class TicketIn(BaseModel):
    ticket_text: str

    class Config:
        schema_extra = {
            "example": {
                "ticket_text": "My production server is down and customers are affected"
            }
        }


class TicketOut(BaseModel):
    priority: str
    intent: str
    confidence_score: float
    response: str
    reason: str
    suggested_actions: List[str]
    raw: str = ""

    class Config:
        schema_extra = {
            "example": {
                "priority": "Urgent",
                "intent": "Production outage",
                "confidence_score": 0.92,
                "response": "Thanks for reporting this. Our team is investigating.",
                "reason": "Production-impacting keywords detected",
                "suggested_actions": [
                    "Check server logs",
                    "Verify service health",
                    "Notify on-call engineer"
                ],
                "raw": "mock response"
            }
        }


@router.post("/classify", response_model=TicketOut)
async def classify_ticket(payload: TicketIn):
    llm = LLMClient()
    result = llm.classify_ticket(payload.ticket_text)

    return TicketOut(
        priority=result.get("priority", "unknown"),
        intent=result.get("intent", ""),
        confidence_score=result.get("confidence_score", 0.0),
        response=result.get("response", ""),
        reason=result.get("reason", ""),
        suggested_actions=result.get("suggested_actions", []),
        raw=result.get("raw", "")
    )
