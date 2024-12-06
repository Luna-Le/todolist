import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config
from app.main import app
from app.config import settings
from app.database import Base, get_db
from app.oauth2 import create_access_token
from app.models import User
from passlib.context import CryptContext

# Database URL remains the same
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:5434/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def apply_migrations():
    """Applies migrations at beginning of testing session"""
    config = Config("alembic.ini")
    
    # Make sure we're using test database
    config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
    
    # Run the migrations
    command.upgrade(config, "head")
    yield
    # Optionally, downgrade all migrations at the end of testing session
    command.downgrade(config, "base")

# @pytest.fixture(scope="function")
# def session(apply_migrations):
#     # Clear all tables before each test
#     for tbl in reversed(Base.metadata.sorted_tables):
#         engine.execute(tbl.delete()) #deprecated
    
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@pytest.fixture(scope="function")
def session():
    # Create tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rest of your fixtures remain the same
@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
            
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture
def test_user(session):
    user_data = {
        "email": "test@example.com",
        "password": pwd_context.hash("password123")  # Hash the password!
    }
    user = User(**user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user.id})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_user_data():
    return {
        "email": "test@example.com",
        "password": "password123"  # Plain password for testing login
    }