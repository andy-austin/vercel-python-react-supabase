from fastapi.testclient import TestClient

from apps.api.index import app

client = TestClient(app)


class TestHealthEndpoint:
    def test_health_endpoint_returns_ok(self):
        """Test that the health endpoint returns OK status"""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    def test_health_endpoint_content_type(self):
        """Test that the health endpoint returns JSON content type"""
        response = client.get("/health")

        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]


class TestGraphQLHealthQuery:
    def test_health_query_basic(self):
        """Test basic GraphQL health query"""
        query = """
        query {
            health {
                status
                timestamp
                api {
                    status
                }
                database {
                    status
                    connection
                }
            }
        }
        """

        response = client.post("/graphql", json={"query": query})

        assert response.status_code == 200
        data = response.json()

        # Check that we have no errors
        assert "errors" not in data or not data["errors"]

        # Check the structure of the response
        health_data = data["data"]["health"]
        assert "status" in health_data
        assert "timestamp" in health_data
        assert "api" in health_data
        assert "database" in health_data

        # Check API status
        assert "status" in health_data["api"]

        # Check database status
        assert "status" in health_data["database"]
        assert "connection" in health_data["database"]

    def test_health_query_returns_valid_status(self):
        """Test that health query returns valid status values"""
        query = """
        query {
            health {
                status
                api {
                    status
                }
                database {
                    status
                }
            }
        }
        """

        response = client.post("/graphql", json={"query": query})

        assert response.status_code == 200
        data = response.json()
        health_data = data["data"]["health"]

        # Valid status values
        valid_statuses = ["ok", "degraded", "error"]

        assert health_data["status"] in valid_statuses
        assert health_data["api"]["status"] in valid_statuses
        assert health_data["database"]["status"] in valid_statuses

    def test_graphql_endpoint_accessible(self):
        """Test that the GraphQL endpoint is accessible"""
        # Send an introspection query to test basic GraphQL functionality
        query = """
        query {
            __schema {
                types {
                    name
                }
            }
        }
        """

        response = client.post("/graphql", json={"query": query})

        assert response.status_code == 200
        data = response.json()

        # Check that we have no errors and got schema data
        assert "errors" not in data or not data["errors"]
        assert "data" in data
        assert "__schema" in data["data"]

    def test_invalid_graphql_query(self):
        """Test that invalid GraphQL queries return appropriate errors"""
        query = """
        query {
            invalidField {
                nonExistentField
            }
        }
        """

        response = client.post("/graphql", json={"query": query})

        assert response.status_code == 200
        data = response.json()

        # Should have errors for invalid query
        assert "errors" in data
        assert len(data["errors"]) > 0
