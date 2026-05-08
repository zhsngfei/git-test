from fastapi.testclient import TestClient
import pytest
from pydantic import ValidationError

from app.core.config import Settings
from app.main import app


def test_health_returns_ok() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["appEnv"] == "local"


def test_readiness_reports_local_placeholder_state_without_secrets() -> None:
    client = TestClient(app)
    response = client.get("/health/readiness")

    assert response.status_code == 200
    body = response.json()
    assert body == {
        "status": "ok",
        "appEnv": "local",
        "services": {
            "supabaseAuth": "placeholder",
            "supabaseCollections": "memory",
            "mimoai": "placeholder",
        },
    }
    response_text = response.text
    assert "replace-with-service-role-key" not in response_text
    assert "replace-with-supabase-jwt-secret" not in response_text


def test_cors_allows_configured_frontend_origin() -> None:
    client = TestClient(app)
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_non_local_settings_reject_placeholder_secrets() -> None:
    with pytest.raises(ValidationError):
        Settings(app_env="production")
