import pytest

@pytest.mark.integration
def test_complete_task_flow(authorized_client, test_user):
    # 1. Create a task
    create_response = authorized_client.post(
        "/tasks", 
        json={
            "name": "Integration Test Task",
            "completed": "false",
        }
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]
    
    # 2. Get the task
    get_response = authorized_client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Integration Test Task"
    
    # 3. Update the task
    update_response = authorized_client.put(
        f"/tasks/{task_id}",
        json={
            "name": "Updated Task",
            "completed": "true",
            "category": "Updated Category"
        }
    )
    assert update_response.status_code == 200
    
    # 4. Verify the update
    get_updated = authorized_client.get(f"/tasks/{task_id}")
    assert get_updated.json()["completed"] == True
    
    # 5. Delete the task
    delete_response = authorized_client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204
    
    # 6. Verify deletion
    get_deleted = authorized_client.get(f"/tasks/{task_id}")
    assert get_deleted.status_code == 404