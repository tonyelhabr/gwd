# import pytest

# @pytest.fixture
# def test_venue_data():
#     return {
#         "source_id": "new_source",
#         "name": "New Venue",
#         "lat": 123.45,
#         "lon": 678.90,
#         "address": "123 New St",
#         "url": "http://newvenue.com"
#     }

# def test_create_venue_success(client, test_venue_data):
#     response = client.post("/api/venues/", json=test_venue_data)

#     assert response.status_code == 201
#     assert response.json()["source_id"] == test_venue_data["source_id"]

# def test_create_venue_fail_duplicate(client, test_venue_data):
#     response = client.post("/api/venues/", json=test_venue_data)
#     assert response.status_code == 201
    
#     duplicate_data = {
#         "source_id": test_venue_data["source_id"],
#         "name": "Existing Venue",
#         "lat": 123.45,
#         "lon": 678.90,
#         "address": "123 Existing St",
#         "url": "http://existingvenue.com"
#     }

#     response = client.post("/api/venues/", json=duplicate_data)

#     assert response.status_code == 400
#     assert "already used" in response.json()["detail"]
