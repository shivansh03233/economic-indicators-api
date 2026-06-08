# 📊 Economic Indicators REST API

A production-ready REST API for macroeconomic data — inflation, GDP growth, unemployment, interest rates, and more. Built with **FastAPI**, **SQLAlchemy**, and an in-memory TTL cache (Redis-ready).

[![CI](https://github.com/YOUR_USERNAME/eco-indicators-api/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/eco-indicators-api/actions)

---

## Architecture

```
┌─────────────┐     HTTP      ┌──────────────────────────────────┐
│   Client    │ ────────────▶ │         FastAPI App              │
└─────────────┘               │  ┌──────────┐  ┌─────────────┐  │
                               │  │  Routes  │  │  TTL Cache  │  │
                               │  └────┬─────┘  └─────────────┘  │
                               │       │                          │
                               │  ┌────▼──────────────────────┐  │
                               │  │  SQLAlchemy ORM (SQLite /  │  │
                               │  │  PostgreSQL)               │  │
                               │  └────────────────────────────┘  │
                               │       │                          │
                               │  ┌────▼─────────────────────┐   │
                               │  │  World Bank Open Data API │   │
                               │  └──────────────────────────┘   │
                               └──────────────────────────────────┘
```

---

## Features

- **5 macroeconomic indicators** — inflation, GDP growth, unemployment, interest rate, current account
- **Multi-country support** — US, India, UK, Germany, Japan, China
- **Live data fetching** from World Bank Open Data API (no API key required)
- **TTL caching** — 1-hour in-memory cache, drop-in Redis upgrade path
- **Full CRUD** — create, read, delete indicator records
- **Auto-generated Swagger docs** at `/docs`
- **Docker support** + GitHub Actions CI

---

## Quick Start

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/eco-indicators-api.git
cd eco-indicators-api

# Install
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload

# Open docs
open http://localhost:8000/docs
```

### Docker

```bash
docker build -t eco-api .
docker run -p 8000:8000 eco-api
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/api/v1/indicators/supported` | List all supported indicators |
| `GET` | `/api/v1/indicators` | List stored records (filterable) |
| `GET` | `/api/v1/indicators/summary` | Latest value + change per indicator |
| `GET` | `/api/v1/indicators/{indicator}` | Time-series for one indicator |
| `POST` | `/api/v1/indicators` | Manually insert a record |
| `POST` | `/api/v1/indicators/fetch` | Fetch live data from World Bank |
| `DELETE` | `/api/v1/indicators/{id}` | Delete a record |
| `GET` | `/api/v1/cache/stats` | Inspect cache state |

### Example: Fetch live US inflation data

```bash
curl -X POST "http://localhost:8000/api/v1/indicators/fetch?indicator=inflation&country=US&years=10"
```

### Example: Get summary for India

```bash
curl "http://localhost:8000/api/v1/indicators/summary?country=IN"
```

---

## Supported Indicators

| Key | Description | Unit |
|-----|-------------|------|
| `inflation` | Consumer Price Index, annual % | % |
| `gdp_growth` | GDP Growth Rate, annual % | % |
| `unemployment` | Unemployment Rate | % |
| `interest_rate` | Real Interest Rate | % |
| `current_account` | Current Account Balance | % GDP |

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Upgrading to Redis Cache

In `app/services/cache.py`, swap the in-memory store for Redis in 3 lines:

```python
import redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def cache_get(key): return json.loads(r.get(key)) if r.get(key) else None
def cache_set(key, value, ttl=3600): r.setex(key, ttl, json.dumps(value))
```

---

## Tech Stack

- **FastAPI** — async REST framework
- **SQLAlchemy** — ORM with SQLite (dev) / PostgreSQL (prod)
- **httpx** — async HTTP client for upstream API calls
- **Pydantic v2** — request/response validation
- **Pytest** — test suite
- **Docker** — containerisation
- **GitHub Actions** — CI/CD

---

## Author

**Shivansh Shukla** — [Shivanshshukla304@gmail.com](mailto:Shivanshshukla304@gmail.com)
