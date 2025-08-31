from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "GraphQL API is running"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_graphql_query():
    query = {"query": "{ hello }"}
    response = client.post("/", json=query)
    assert response.status_code == 200
    assert "hello" in response.json()["data"]
