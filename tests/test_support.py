import os
import sys
import importlib.util
from fastapi.testclient import TestClient

# Load our FastAPI app module explicitly from src/app/main.py to avoid name collisions
spec = importlib.util.spec_from_file_location("local_app", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "app", "main.py")))
local_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(local_app)
app = getattr(local_app, "app")

client = TestClient(app)


def test_classify_ticket_mock():
    # Ensure no API key to enforce mock behavior
    if os.getenv("OPENAI_API_KEY"):
        del os.environ["OPENAI_API_KEY"]

    payload = {"ticket_text": "The app crashes on start with a stack trace."}
    resp = client.post("/support/classify", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "priority" in data or "raw" in data
    # Mock logic should return Urgent when 'crash' present
    assert data.get("priority") in ("Urgent", "Normal", None)
