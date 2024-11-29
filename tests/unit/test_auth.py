import pytest
from app.models import User



@pytest.mark.auth
def test_login(client, test_user_data, test_user):
    response = client.post(
        "/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]  # Use plain password for login
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.auth
def test_login_invalid_credentials(client, test_user_data, test_user):
    response = client.post(
        "/login",
        data={
            "username": "test@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 403

@pytest.mark.auth
def test_login_user_not_found(client, test_user_data, test_user):
    response = client.post("/login", data={"username": "nonexistent@test.com", "password": "password123"})
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid Credentials"
