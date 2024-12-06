from app.models import User
import pytest

@pytest.mark.user
def test_create_user(client):
    response = client.post("/users", json={"email": "test5@test.com", "password": "password"})
    assert response.status_code == 201
    assert response.json()["email"] == "test5@test.com"


@pytest.mark.user
def test_get_user(client, test_user):
    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

