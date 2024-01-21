from unittest.mock import MagicMock
from app.crud.venues import create_venue
from app.db.models import Venue
from app.db.schemas import VenueCreate
import pytest

@pytest.fixture
def mock_session():
    session = MagicMock()
    session.add = MagicMock()
    session.commit = MagicMock()
    session.refresh = MagicMock()
    return session

def test_create_venue(mock_session):
    # Define test data
    test_venue = VenueCreate(
        source_id="test_source",
        name="Test Venue",
        lat=123.45,
        lon=678.90,
        address="123 Test St",
        url="http://testvenue.com"
    )

    # Call the function
    result = create_venue(mock_session, test_venue)

    # Assert expected outcomes
    assert isinstance(result, Venue)
    assert result.source_id == test_venue.source_id
    assert result.name == test_venue.name

    # Optionally, assert that the correct session methods were called
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(result)
