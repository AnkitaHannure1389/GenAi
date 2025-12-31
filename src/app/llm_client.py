# 

# src/app/llm_client.py
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
            # Run in mock mode for local development and tests
            self.mock = True
        else:
            openai.api_key = self.api_key

    def classify_ticket(self, ticket_text: str) -> Dict[str, Any]:
        """
        Classify a support ticket and generate an initial response.
        Returns a dict with keys: priority, response, reason, raw.
        """
        if self.mock:
            # Deterministic mock response for local dev/testing
            priority = "Urgent" if "crash" in ticket_text.lower() else "Normal"
            return {
                "priority": priority,
                "response": "Thanks for reporting this. We are investigating.",
                "reason": "Detected crash-like keywords",
                "raw": "mock response",
            }

        system_msg = (
            "You are an expert technical support agent. "
            "Classify the ticket by priority and generate a short first response. "
            "Return output as a JSON object with keys: priority (Urgent|Normal|Low), response, reason."
        )
        user_msg = f"Ticket:\n{ticket_text}\n\nRespond only with a JSON object."

        try:
            resp = openai.responses.create(
                model=self.model,
                input=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.0,
                max_output_tokens=300,
            )

            # Extract text output
            out = ""
            try:
                out = resp.output[0].content[0].text
            except Exception:
                out = getattr(resp, "output_text", "") or str(resp)

            # Extract JSON from model output
            match = re.search(r"(\{.*\})", out, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group(1))
                    # Ensure all keys exist
                    data.setdefault("priority", "unknown")
                    data.setdefault("response", "")
                    data.setdefault("reason", "")
                    data.setdefault("raw", out)
                    return data
                except json.JSONDecodeError:
                    pass

            return {"priority": "unknown", "response": "", "reason": "", "raw": out}

        except Exception as e:
            return {
                "priority": "unknown",
                "response": "",
                "reason": str(e),
                "raw": str(e),
            }
