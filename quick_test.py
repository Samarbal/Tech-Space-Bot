# quick_test.py
import asyncio
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)
response = client.post("/ask", json={"question": "Which product has the longest battery life?"})
print(response.json()["answer"])