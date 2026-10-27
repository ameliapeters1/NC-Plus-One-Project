def test_get_events_returns_everything(client):
    response = client.get(f"/api/events")
    assert response.status_code == 200
    assert len(response.json()["events"]) == 10