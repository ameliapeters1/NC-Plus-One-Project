from fetch_info.rsvp import get_rsvp

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
    assert response.json()["error"]["code"] == "Not Authenticated"

def test_rsvp_with_invalid_event_raises_401(client, valid_test_login):
    token = valid_test_login
    response = client.post("/api/events/999999/rsvp", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "Not Found"

def test_duplicate_rsvp_raises_409(client, valid_test_login):
    token = valid_test_login
    response = client.post("/api/events/1/rsvp", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "Conflict"

def test_delete_rsvp_deletes_rsvp(client, valid_test_login):
    token = valid_test_login
    response = client.delete("/api/events/1/rsvp/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204

    rsvp_present = get_rsvp(2,1)
    assert rsvp_present is None

def test_delete_rsvp_with_invalid_token_raises_401(client):
    token = "invalidtoken"
    response = client.delete("/api/events/1/rsvp/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "Not Authenticated"

def test_delete_rsvp_that_doesnt_exist_raises_404(client, valid_test_login):
    token = valid_test_login
    response = client.delete("/api/events/9/rsvp/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "Not Found"

def test_create_event_creates_event(client, valid_test_login):
    token = valid_test_login
    response = client.post("/api/events", headers={"Authorization": f"Bearer {token}"},
                           json={"title": "test event",
                                 "description": "testing",
                                 "starts_at": "2026-07-22T18:00:00+01:00",
                                 "ends_at":"2026-07-22T19:00:00+01:00",
                                 "venue_id":1
                                 },)
    assert response.status_code == 201

def test_create_event_with_invalid_token_raises_401(client):
    token = "invalidtoken"
    response = client.post("/api/events", headers={"Authorization": f"Bearer {token}"},
                           json={"title": "test event",
                                 "description": "testing",
                                 "starts_at": "2026-10-30T12:08:49.500Z",
                                 "ends_at":"2026-10-30T12:08:49.521Z",
                                 "venue_id":1
                                 },)
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "Not Authenticated"

def test_create_event_with_missing_title_raises_400(client,valid_test_login):
    token = valid_test_login
    response = client.post("/api/events", headers={"Authorization": f"Bearer {token}"},
                           json={"title": "",
                                 "description": "testing",
                                 "starts_at": "2026-10-30T12:08:49.500Z",
                                 "ends_at":"2026-10-30T12:08:49.521Z",
                                 "venue_id":1
                                 },)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "Bad Request"

def test_create_event_with_missing_start_raises_400(client,valid_test_login):
    token = valid_test_login
    response = client.post("/api/events", headers={"Authorization": f"Bearer {token}"},
                           json={"title": "test event",
                                 "description": "testing",
                                 "starts_at": "",
                                 "ends_at":"2026-10-30T12:08:49.521Z",
                                 "venue_id":1
                                 },)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "Bad Request"

def test_create_event_with_missing_end_raises_400(client,valid_test_login):
    token = valid_test_login
    response = client.post("/api/events", headers={"Authorization": f"Bearer {token}"},
                           json={"title": "test event",
                                 "description": "testing",
                                 "starts_at": "2026-10-30T12:08:49.521Z",
                                 "ends_at":"",
                                 "venue_id":1
                                 },)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "Bad Request"


def test_create_event_with_not_valid_venue_raises_404(client,valid_test_login):
    token = valid_test_login
    response = client.post("/api/events", headers={"Authorization": f"Bearer {token}"},
                           json={"title": "test event",
                                 "description": "testing",
                                 "starts_at": "2026-10-30T12:08:49.500Z",
                                 "ends_at":"2026-10-30T12:08:49.521Z",
                                 "venue_id":999999
                                 },)
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "Not Found"

def test_create_event_with_not_valid_venue_raises_404(client,valid_test_login):
    token = valid_test_login
    response = client.post("/api/events", headers={"Authorization": f"Bearer {token}"},
                           json={"title": "test event",
                                 "description": "testing",
                                 "starts_at": "2026-10-30T12:08:49.500Z",
                                 "ends_at":"2026-10-29T12:08:49.521Z",
                                 "venue_id":1
                                 },)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "Bad Request"