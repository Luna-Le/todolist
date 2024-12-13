import pytest
from app.models import Task, User


@pytest.fixture
def test_user2(session):
    user2 = User(
        email="user2@example.com",
        password="password123",
    )
    session.add(user2)
    session.commit()
    return user2

@pytest.fixture
def test_task(session, test_user):  # Add test_user dependency
 


    task = Task(owner_id=test_user.id, name="Test Task", completed=False)
    session.add(task)
    session.commit()
    return task

@pytest.fixture
def test_task2(session, test_user2):  # Add test_user2 dependency

  

    task = Task(owner_id=test_user2.id, name="Test Task2", completed=False)
    session.add(task)
    session.commit()
    return task

@pytest.mark.task
def test_create_task(session, test_user, authorized_client):
    response = authorized_client.post("/tasks", json={"name": "Test Task3", "completed": "false"})
   
    assert response.status_code == 201
    assert response.json()["name"] == "Test Task3"
    assert response.json()["completed"] == False
  



@pytest.mark.task
def test_get_task(authorized_client, test_task):
    response = authorized_client.get(f"/tasks/{test_task.id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Task"
    assert response.json()["completed"] == False    



@pytest.mark.task
def test_get_task_not_found(authorized_client):
    response = authorized_client.get("/tasks/3")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with id: 3 was not found"

@pytest.mark.task
def test_get_task_unauthorized(authorized_client, test_task2):

    response = authorized_client.get(f"/tasks/{test_task2.id}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to perform requested action"


@pytest.mark.task
def test_delete_task(authorized_client, test_task):
    response = authorized_client.delete(f"/tasks/{test_task.id}")
    assert response.status_code == 204

@pytest.mark.task
def test_delete_task_not_found(authorized_client):
    response = authorized_client.delete("/tasks/3")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with id: 3 was not found"

@pytest.mark.task
def test_delete_task_unauthorized(authorized_client, test_task2):
    response = authorized_client.delete(f"/tasks/{test_task2.id}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to perform requested action"

@pytest.mark.task
def test_get_tasks(authorized_client, test_task ):
    response = authorized_client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  
    assert len(response.json()) > 0  


@pytest.mark.task
def test_update_task(authorized_client, test_task):
    response = authorized_client.put(f"/tasks/{test_task.id}", json={"name": "Updated Task", "completed": "true"})


    assert response.status_code == 200
    assert response.json()["name"] == "Updated Task"
    assert response.json()["completed"] == True

