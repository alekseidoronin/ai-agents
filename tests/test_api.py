from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# --- System ---

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert "version" in body


# --- Users ---

def test_list_users():
    response = client.get("/api/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_user():
    import uuid
    tid = f"test_{uuid.uuid4().hex[:8]}"
    response = client.post(
        "/api/users/",
        json={"telegram_id": tid, "username": "testuser", "first_name": "Test"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["telegram_id"] == tid
    assert data["username"] == "testuser"
    assert data["is_active"] is True


def test_create_user_duplicate():
    import uuid
    tid = f"dup_{uuid.uuid4().hex[:8]}"
    client.post("/api/users/", json={"telegram_id": tid})
    response = client.post("/api/users/", json={"telegram_id": tid})
    assert response.status_code == 409


def test_get_user_by_telegram():
    import uuid
    tid = f"lookup_{uuid.uuid4().hex[:8]}"
    client.post("/api/users/", json={"telegram_id": tid})
    response = client.get(f"/api/users/telegram/{tid}")
    assert response.status_code == 200
    assert response.json()["telegram_id"] == tid


def test_get_user_not_found():
    response = client.get("/api/users/999999")
    assert response.status_code == 404


# --- Content Plans ---

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
    assert "created_at" in data


def test_get_content_plan():
    create = client.post(
        "/api/content-plans/",
        json={"product_name": "GetTest", "target_audience": "QA"},
    )
    plan_id = create.json()["id"]
    response = client.get(f"/api/content-plans/{plan_id}")
    assert response.status_code == 200
    assert response.json()["product_name"] == "GetTest"


def test_delete_content_plan():
    create = client.post(
        "/api/content-plans/",
        json={"product_name": "ToDelete", "target_audience": "Nobody"},
    )
    plan_id = create.json()["id"]
    response = client.delete(f"/api/content-plans/{plan_id}")
    assert response.status_code == 204
    get = client.get(f"/api/content-plans/{plan_id}")
    assert get.status_code == 404


def test_content_plan_not_found():
    response = client.get("/api/content-plans/999999")
    assert response.status_code == 404


# --- Sales Funnels ---

def test_list_sales_funnels():
    response = client.get("/api/sales-funnels/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_sales_funnel():
    response = client.post(
        "/api/sales-funnels/",
        json={
            "product_name": "SaaS Tool",
            "funnel_type": "webinar",
            "target_audience": "Startups",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["product_name"] == "SaaS Tool"
    assert data["funnel_type"] == "webinar"


def test_delete_sales_funnel():
    create = client.post(
        "/api/sales-funnels/",
        json={
            "product_name": "DeleteMe",
            "target_audience": "Nobody",
        },
    )
    funnel_id = create.json()["id"]
    response = client.delete(f"/api/sales-funnels/{funnel_id}")
    assert response.status_code == 204


def test_sales_funnel_not_found():
    response = client.get("/api/sales-funnels/999999")
    assert response.status_code == 404


# --- OpenAPI docs ---

def test_openapi_docs():
    response = client.get("/docs")
    assert response.status_code == 200
