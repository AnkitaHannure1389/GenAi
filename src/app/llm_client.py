import os
import json
import re
from typing import Any, Dict

try:
    import openai
except Exception:
    openai = None


class LLMClient:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.mock = False

        if not self.api_key or openai is None:
            self.mock = True
        else:
            openai.api_key = self.api_key

    def classify_ticket(self, ticket_text: str) -> Dict[str, Any]:

        # ---------------- MOCK MODE ----------------
        if self.mock:
            return {
                "priority": "Urgent" if "down" in ticket_text.lower() else "Normal",
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

        # ---------------- LLM MODE ----------------
        system_msg = (
            "You are an expert technical support agent.\n"
            "Return ONLY a JSON object with:\n"
            "priority (Urgent|Normal|Low), intent, confidence_score (0-1), "
            "response, reason, suggested_actions"
        )

        user_msg = f"Ticket:\n{ticket_text}"

        try:
            resp = openai.responses.create(
                model=self.model,
                input=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.0,
                max_output_tokens=400,
            )

            try:
                out = resp.output[0].content[0].text
            except Exception:
                out = getattr(resp, "output_text", "") or str(resp)

            match = re.search(r"(\{.*\})", out, re.DOTALL)
            if match:
                data = json.loads(match.group(1))
                data.setdefault("confidence_score", 0.0)
                data.setdefault("suggested_actions", [])
                data["raw"] = out
                return data

            return {
                "priority": "unknown",
                "intent": "",
                "confidence_score": 0.0,
                "response": "",
                "reason": "Invalid JSON from model",
                "suggested_actions": [],
                "raw": out,
            }

        except Exception as e:
            return {
                "priority": "unknown",
                "intent": "",
                "confidence_score": 0.0,
                "response": "",
                "reason": str(e),
                "suggested_actions": [],
                "raw": str(e),
            }
