# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# import importlib.util
# import os

# # Load local llm_client module by file path to avoid name collisions with other 'app' modules
# spec = importlib.util.spec_from_file_location("local_llm_client", os.path.join(os.path.dirname(__file__), "..", "llm_client.py"))
# llm_client_mod = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(llm_client_mod)
# LLMClient = llm_client_mod.LLMClient

# router = APIRouter()

# class TicketIn(BaseModel):
#     ticket_text: str

# class TicketOut(BaseModel):
#     priority: str | None = None
#     response: str | None = None
#     reason: str | None = None
#     raw: str | None = None

# llm = LLMClient()

# @router.post("/support/classify", response_model=TicketOut)
# def classify_ticket(data: TicketIn):
#     try:
#         result = llm.classify_ticket(data.ticket_text)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     return result


# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel, Field

# from src.app.llm_client import LLMClient
# from src.app.prompt import SYSTEM_PROMPT

# from app.safety import sanitize_input


# router = APIRouter(prefix="/support", tags=["Support"])

# llm_client = LLMClient()


# # ---------
# # Request / Response Schemas
# # ---------

# class TicketIn(BaseModel):
#     ticket_text: str = Field(
#         ...,
#         description="Customer support ticket text",
#         example="My production server is down and customers are affected"
#     )


# class TicketOut(BaseModel):
#     priority: str
#     response: str
#     reason: str | None = None
#     raw: str | None = None


# # ---------
# # Routes
# # ---------

# @router.post("/classify", response_model=TicketOut)
# def classify_ticket(payload: TicketIn):
#     """
#     Classify a support ticket and generate a safe first response.
#     """

#     # 1. Sanitize input (guardrail)
#     clean_text = sanitize_input(payload.ticket_text)

#     # 2. Build user prompt
#     user_prompt = f"""
#     Customer support ticket:
#     \"\"\"{clean_text}\"\"\"

#     Tasks:
#     1. Classify priority as one of: Urgent, Normal, Low
#     2. Generate a short, professional first response
#     3. Explain briefly why this priority was chosen

#     Return JSON with keys:
#     priority, response, reason
#     """

#     try:
#         # 3. Call LLM
#         llm_result = llm_client.generate(
#             system_prompt=SYSTEM_PROMPT,
#             user_prompt=user_prompt
#         )

#         return TicketOut(
#             priority=llm_result.get("priority", "Low"),
#             response=llm_result.get("response", "Unable to generate response."),
#             reason=llm_result.get("reason"),
#             raw=str(llm_result)
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter
from pydantic import BaseModel
from src.app.llm_client import LLMClient

router = APIRouter(prefix="/support", tags=["support"])


class TicketIn(BaseModel):
    ticket_text: str


class TicketOut(BaseModel):
    priority: str
    response: str
    reason: str
    raw: str = ""


@router.post("/classify", response_model=TicketOut)
async def classify_ticket(payload: TicketIn):
    llm = LLMClient()

    try:
        # Correct method: classify_ticket
        result = llm.classify_ticket(payload.ticket_text)

        return TicketOut(
            priority=result.get("priority", "unknown"),
            response=result.get("response", ""),
            reason=result.get("reason", ""),
            raw=result.get("raw", "")
        )

    except Exception as e:
        return TicketOut(
            priority="unknown",
            response="We are unable to classify your ticket at the moment.",
            reason=str(e),
            raw=str(e)
        )
