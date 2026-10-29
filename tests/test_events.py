def test_get_events_returns_everything(client):
    response = client.get(f"/api/events")
    assert response.status_code == 200
    assert len(response.json()["events"]) == 10

def test_get_event_by_id_returns_existing_event(client):
    response = client.get(f"/api/events/{2}")
    assert response.status_code == 200
    assert response.json()["event"]["id"] == 2

def test_get_event_not_found_returns_404(client):
    response = client.get("/api/events/999999")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "Not Found"

def test_get_event_invalid_int_returns_404(client):
    response = client.get("/api/events/-1")
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "Bad Request"


def test_event_rsvp_creates_rsvp(client, valid_test_login):
    token = valid_test_login
    response = client.post("/api/events/9/rsvp", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["rsvp"]["attendee_id"] == 2
    assert response.json()["rsvp"]["event_id"] == 9


def test_rsvp_with_invalid_token_raises_401(client):
    token = "invalidtoken"
    response = client.post("/api/events/9/rsvp", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json()["code"] == "Not Authenticated"

def test_rsvp_with_invalid_token_raises_401(client, valid_test_login):
    token = valid_test_login
    response = client.post("/api/events/999999/rsvp", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "Not Found"

def test_duplicate_rsvp_raises_409(client, valid_test_login):
    token = valid_test_login
    response = client.post("/api/events/1/rsvp", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "Conflict"