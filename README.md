# Support & Contract Review PoC (5-step AI training project)

This repository demonstrates the 5-step workflow: translate a business problem to an AI task, select a model, create a PoC prompt, integrate it via API, and add monitoring.

Quick start

1. Create a Python environment (3.11+).
2. Set your OpenAI API key in an env var: `OPENAI_API_KEY`.
3. Install dependencies:

   pip install -r requirements.txt

4. Run the FastAPI app:

   uvicorn src.app.main:app --reload

5. Example:

   curl -X POST "http://127.0.0.1:8000/support/classify" -H "Content-Type: application/json" -d '{"ticket_text": "My app crashes on start with error code 500"}'

Notes

- If `OPENAI_API_KEY` is not set, the `LLMClient` uses a local mock response for testing and development.
- Prompts are stored in `src/app/prompts`.
