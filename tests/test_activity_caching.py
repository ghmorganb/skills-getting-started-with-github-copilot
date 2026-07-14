from fastapi.testclient import TestClient

from src.app import app


def test_activities_endpoint_avoids_stale_browser_caching():
    client = TestClient(app)

    response = client.get("/activities")

    assert response.status_code == 200
    cache_control = response.headers.get("cache-control", "").lower()
    assert "no-store" in cache_control
