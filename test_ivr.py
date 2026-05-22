from fastapi.testclient import TestClient
from backend import app

client = TestClient(app)

def test_voice_endpoint():
    response = client.post("/voice")
    assert response.status_code == 200
    assert "<Gather" in response.text

def test_main_menu_valid():
    response = client.post("/handle_main_menu", data={"Digits": "1"})
    assert response.status_code == 200
    assert "Housekeeping" in response.text

def test_main_menu_invalid():
    response = client.post("/handle_main_menu", data={"Digits": "9"})
    assert "Invalid entry" in response.text