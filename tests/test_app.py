def test_get_activities_returns_initial_data(client):
    """Test that GET /activities returns the initial activities data."""
    # Arrange - fixtures handle setup

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert len(data["Chess Club"]["participants"]) == 2


def test_signup_adds_participant(client):
    """Test that POST /activities/{activity}/signup adds a new participant."""
    # Arrange
    email = "new@student.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Signed up {email} for {activity}"

    # Verify participant was added
    get_response = client.get("/activities")
    activities = get_response.json()
    assert email in activities[activity]["participants"]


def test_signup_duplicate_returns_400(client):
    """Test that signing up a duplicate participant returns 400."""
    # Arrange
    email = "michael@mergington.edu"  # Already in Chess Club
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "already registered" in data["detail"]


def test_signup_full_activity_returns_400(client):
    """Test that signing up for a full activity returns 400."""
    # Arrange - Chess Club has max 12, currently 2, so add 10 more
    activity = "Chess Club"
    for i in range(10):
        email = f"student{i}@edu"
        client.post(f"/activities/{activity}/signup", params={"email": email})

    # Now it's full (12 participants)
    email = "last@student.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "full" in data["detail"]


def test_remove_participant_removes(client):
    """Test that DELETE /activities/{activity}/participants/{email} removes a participant."""
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Removed {email} from {activity}"

    # Verify participant was removed
    get_response = client.get("/activities")
    activities = get_response.json()
    assert email not in activities[activity]["participants"]


def test_remove_nonexistent_returns_404(client):
    """Test that removing a nonexistent participant returns 404."""
    # Arrange
    email = "nonexistent@edu"
    activity = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"]


def test_signup_invalid_activity_returns_404(client):
    """Test that signing up for invalid activity returns 404."""
    # Arrange
    email = "test@edu"
    activity = "Invalid Activity"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"]
