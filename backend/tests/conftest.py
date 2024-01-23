from app.main import app
from fastapi.testclient import TestClient
import pytest

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.config import Settings
from app.db.database import Base, get_db

settings = Settings()

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture
def client()-> TestClient:
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def test_venue_data():
    return {
        "source_id": "new_source",
        "name": "New Venue",
        "lat": 123.45,
        "lon": 678.90,
        "address": "123 New St",
        "url": "http://newvenue.com"
    }

def test_create_venue_success(client, test_venue_data):
    response = client.post("/api/venues/", json=test_venue_data)

    assert response.status_code == 201
    assert response.json()["source_id"] == test_venue_data["source_id"]
