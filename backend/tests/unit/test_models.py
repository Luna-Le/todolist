from app.models import User, Task, Category

def test_user_model():
    user = User(email="test@test.com", password="password")
    assert user.email == "test@test.com" 
    assert user.password == "password"

def test_task_model(): 
   
    category = Category(name="test")

    task = Task(
        name="test", 
        completed=False, 
        category=category,  
        owner_id=1  
    )
    
    assert task.name == "test"
    assert task.completed == False
    assert task.category.name == "test"

def test_category_model():
    category = Category(name="work")
    assert category.name == "work"
