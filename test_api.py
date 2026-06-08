import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Use in-memory SQLite for tests
TEST_DB_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_supported_indicators():
    resp = client.get("/api/v1/indicators/supported")
    assert resp.status_code == 200
    data = resp.json()
    assert "inflation" in data
    assert "gdp_growth" in data


def test_create_and_retrieve_indicator():
    payload = {
        "indicator": "inflation",
        "country": "US",
        "value": 3.4,
        "period": "2023",
        "unit": "%",
        "source": "test",
    }
    resp = client.post("/api/v1/indicators", json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert body["indicator"] == "inflation"
    assert body["value"] == 3.4
    record_id = body["id"]

    # Retrieve via list endpoint
    resp2 = client.get("/api/v1/indicators?indicator=inflation&country=US")
    assert resp2.status_code == 200
    assert resp2.json()["total"] >= 1

    # Retrieve via named endpoint
    resp3 = client.get("/api/v1/indicators/inflation?country=US")
    assert resp3.status_code == 200

    # Delete
    resp4 = client.delete(f"/api/v1/indicators/{record_id}")
    assert resp4.status_code == 204


def test_summary_empty():
    resp = client.get("/api/v1/indicators/summary?country=US")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_cache_stats():
    resp = client.get("/api/v1/cache/stats")
    assert resp.status_code == 200
    assert "active_keys" in resp.json()


def test_fetch_invalid_indicator():
    resp = client.post("/api/v1/indicators/fetch?indicator=fake_indicator&country=US")
    assert resp.status_code == 400
