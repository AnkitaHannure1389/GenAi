# from app.llm_client import LLMClient

# if __name__ == "__main__":
#     client = LLMClient()
#     sample = "My application crashes on startup with error 500. Steps to reproduce: open app, click sync."
#     print(client.classify_ticket(sample))


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROMPT_PATH = BASE_DIR / "prompts" / "support_ticket.txt"

with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()
