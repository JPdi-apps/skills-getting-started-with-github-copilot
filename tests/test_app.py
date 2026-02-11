import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data

def test_signup_and_unregister():
    # Use a unique email to avoid conflicts
    activity = "Basketball"
    email = "pytestuser@mergington.edu"
    # Signup
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200 or resp.status_code == 400  # 400 if already signed up
    # Unregister
    resp2 = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp2.status_code == 200 or resp2.status_code == 400  # 400 if not signed up

def test_signup_invalid_activity():
    resp = client.post("/activities/Nonexistent/signup", params={"email": "nobody@mergington.edu"})
    assert resp.status_code == 404

def test_unregister_invalid_activity():
    resp = client.post("/activities/Nonexistent/unregister", params={"email": "nobody@mergington.edu"})
    assert resp.status_code == 404

def test_unregister_not_signed_up():
    activity = "Basketball"
    email = "notregistered@mergington.edu"
    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 400
