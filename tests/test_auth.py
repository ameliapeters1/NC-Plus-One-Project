from db.connection import get_connection

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

def test_correct_details_registers_user(client):
    response = client.post("/api/auth/register",
                           json={"name": "Steve",
                                 "email": "steve@example.com",
                                 "password": "password123",
                                 },)
    assert response.status_code == 201
    assert response.json()["user"]["name"] == "Steve"
    assert "password" not in response.json()

def test_correct_details_stores_user_in_db(client):
    response = client.post("/api/auth/register",
                           json={"name": "Steve",
                                 "email": "steve@example.com",
                                 "password": "password123",
                                 },)
    assert response.status_code == 201
    try:
    # check details in DB
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users")
            rows = cur.fetchall()
    
        assert len(rows)==7
        # password entry for new user
        assert rows[6][2] != "password123"
    finally:
        conn.close()
    
def test_duplicate_email_raises_error(client):
    response = client.post("/api/auth/register",
                           json={"name": "alice2",
                                 "email": "alice@example.com",
                                 "password": "password1234",
                                 },)
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "Conflict"

def test_missing_name_raises_error(client):
    response = client.post("/api/auth/register",
                           json={"name": "",
                                 "email": "alice@example.com",
                                 "password": "password1234",
                                 },)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "Bad Request"

def test_missing_email_raises_error(client):
    response = client.post("/api/auth/register",
                           json={"name": "Alice",
                                 "email": "",
                                 "password": "password1234",
                                 },)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "Bad Request"

def test_missing_password_raises_error(client):
    response = client.post("/api/auth/register",
                           json={"name": "Alice",
                                 "email": "alice@example.com",
                                 "password": "",
                                 },)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "Bad Request"