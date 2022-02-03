from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
import pytest
from app.oauth2 import create_access_token
from app import models

# LOCAL - MYSQL
SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://root:root@localhost/fastapi_test'

# HEROKU - POSTGRES
# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# FIXTURES
# DB
@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    # run our code before we run our test
    def overrid_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = overrid_get_db
    yield TestClient(app)
    # run our code After our test finishes
    # Base.metadata.drop_all(bind=engine)

# USER
@pytest.fixture
def test_user(client):
    user_data = {"email": "test2@gmail.com", "password": "pass123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

# POSTS
@pytest.fixture
def test_posts(test_user, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    },{
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },{
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }]

    def create_post_model(post):
        return models.Post(**post)
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    
    return posts