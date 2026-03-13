import pytest
from fastapi.testclient import TestClient
from src import app
import copy

# Store initial state of activities
initial_activities = copy.deepcopy(app.activities)

@pytest.fixture
def client():
    """Provides a TestClient for the FastAPI app."""
    return TestClient(app.app)

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the activities dict to initial state before each test."""
    app.activities = copy.deepcopy(initial_activities)
