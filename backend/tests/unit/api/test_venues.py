import pytest

def test_create_venue_success(client, test_venue_data):
    response = client.post("/api/venues/", json=test_venue_data)

    assert response.status_code == 201
    assert response.json()["source_id"] == test_venue_data["source_id"]
