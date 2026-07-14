from fastapi.testclient import TestClient

from src.app import activities, app


def test_activities_endpoint_avoids_stale_browser_caching():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    cache_control = response.headers.get("cache-control", "").lower()
    assert "no-store" in cache_control


def test_signup_endpoint_adds_student_to_activity():
    # Arrange
    client = TestClient(app)
    activity_name = "Chess Club"
    test_email = "new.student@mergington.edu"
    original_participants = list(activities[activity_name]["participants"])

    try:
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email},
        )

        # Assert
        assert response.status_code == 200
        assert test_email in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants
