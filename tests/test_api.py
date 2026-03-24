from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_list_content_plans():
    response = client.get("/api/content-plans/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_content_plan():
    response = client.post(
        "/api/content-plans/",
        json={"product_name": "Test Product", "target_audience": "Developers"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["product_name"] == "Test Product"
    assert data["target_audience"] == "Developers"
