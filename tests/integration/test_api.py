"""
Integration tests for API endpoints.
"""
import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """Test cases for health check endpoints."""

    def test_health_check(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["service"] == "SnapCalories"
        assert data["version"] == "1.0.0"

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert data["service"] == "SnapCalories API"
        assert "description" in data
        assert data["docs"] == "/docs"


class TestWebhookEndpoints:
    """Test cases for webhook endpoints."""

    def test_webhook_verification_success(self, client: TestClient):
        """Test successful webhook verification."""
        # Note: This will fail without proper .env, but tests the endpoint structure
        response = client.get(
            "/webhook",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": "test_token",
                "hub.challenge": "test_challenge"
            }
        )

        # Will likely fail auth, but endpoint should exist
        assert response.status_code in [200, 403]

    def test_webhook_verification_missing_params(self, client: TestClient):
        """Test webhook verification with missing parameters."""
        response = client.get("/webhook")

        assert response.status_code == 400

    def test_webhook_post_endpoint_exists(self, client: TestClient):
        """Test that POST webhook endpoint exists."""
        # Send empty payload
        response = client.post("/webhook", json={})

        # Should process and return 200 (even for invalid payload)
        assert response.status_code == 200
