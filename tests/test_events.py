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