from app import schemas
from app.config import settings
from jose import jwt
import pytest

# TESTS
def test_root(client):
    response = client.get("/")
    print(response.json().get('message'))
    assert response.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={"email": "test2@gmail.com", "password": "pass123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test2@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code",[
    ('wrongemail@gamil.com', 'pass123', 403),
    ('test2@gmail.com', 'wrongPawssword', 403),
    ('wrongemail@gamil.com', 'wrongPawssword', 403), 
    (None, 'pass123', 422),
    ('test2@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json().get('detail') == "Invalid Credentials"

