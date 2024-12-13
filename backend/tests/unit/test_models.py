from app.models import User, Task

def test_user_model():
    user = User(email="test@test.com", password="password")
    assert user.email == "test@test.com" 
    assert user.password == "password"

def test_task_model(): 
   
   

    task = Task(
        name="test", 
        completed=False, 
        owner_id=1  
    )
    
    assert task.name == "test"
    assert task.completed == False



