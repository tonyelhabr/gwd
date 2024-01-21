## https://github.com/testdrivenio/fastapi-crud-sync
import pytest
import app.crud.venues as v
from app.db.schemas import VenueCreate

def test_create_venue(client, monkeypatch):
    new_venue_data = {
        "source_id": "-1",
        "name": "hell",
        "url": "https://helloworld.com",
        "lat": 1.23,
        "lon": 4.56,
        "address": "123 First Street, NYC",
    }
    new_venue = VenueCreate(**new_venue_data)

    def mock_create_venue(db, venue):
        return new_venue

    monkeypatch.setattr(v, "create_venue", mock_create_venue)
    
    result = mock_create_venue(None, new_venue)
    assert result == new_venue
