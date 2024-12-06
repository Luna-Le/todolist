import pytest

@pytest.mark.integration
def test_create_user_flow(client):
    create_response = client.post("/users", json={"email": "test6@test.com", "password": "password"})
    assert create_response.status_code == 201
    assert create_response.json()["email"] == "test6@test.com"
    user_id = create_response.json()["id"]

    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == "test6@test.com"
