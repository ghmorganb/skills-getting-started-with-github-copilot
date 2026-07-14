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


def test_signup_endpoint_rejects_when_activity_is_full():
    # Arrange
    client = TestClient(app)
    activity_name = "Chess Club"
    test_email = "overflow.student@mergington.edu"
    activity = activities[activity_name]
    original_participants = list(activity["participants"])

    try:
        activity["participants"] = [f"student{i}@mergington.edu" for i in range(activity["max_participants"])]

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email},
        )

        # Assert
        assert response.status_code == 400
        assert test_email not in activity["participants"]
    finally:
        activity["participants"] = original_participants
