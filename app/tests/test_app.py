import pytest

from app.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_list_tasks(client):
    response = client.get("/api/tasks")

    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_task(client):
    response = client.post("/api/tasks", json={"title": "Task"})
    assert response.status_code == 201
    assert isinstance(response.json, dict)