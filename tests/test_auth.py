def test_correct_details_returns_token(client):
    response = client.post("/api/auth/login",
                           json={"email": "bob@example.com",
                                 "password": "password123",
                                 },)
    assert response.status_code == 200
    assert "token" in response.json()
    assert isinstance(response.json()["token"], str)

def test_incorrect_email_returns_401(client):
    response = client.post("/api/auth/login",
                               json={"email": "bob@example",
                                     "password": "password123",
                                     },)
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "Unauthorised"


def test_incorrect_password_returns_401(client):
    response = client.post("/api/auth/login",
                               json={"email": "bob@example.com",
                                     "password": "password",
                                     },)
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "Unauthorised"


def test_missing_password_returns_401(client):
    response = client.post("/api/auth/login",
                               json={"email": "bob@example",
                                     "password": "",
                                     },)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "Bad Request"

def test_missing_email_returns_401(client):
    response = client.post("/api/auth/login",
                               json={"email": "",
                                     "password": "password",
                                     },)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "Bad Request"