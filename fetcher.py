"""
Data fetcher service.

Uses the World Bank Open Data API (no API key required) to pull real
macroeconomic indicators. Extend with FRED or Alpha Vantage by adding
your API key to .env.
"""

import httpx
from typing import List, Dict, Any
from datetime import datetime

# World Bank API indicator codes
WB_INDICATORS = {
    "inflation":      {"code": "FP.CPI.TOTL.ZG", "unit": "%",     "name": "Inflation (CPI, annual %)"},
    "gdp_growth":     {"code": "NY.GDP.MKTP.KD.ZG","unit": "%",    "name": "GDP Growth (annual %)"},
    "unemployment":   {"code": "SL.UEM.TOTL.ZS",  "unit": "%",     "name": "Unemployment Rate (%)"},
    "interest_rate":  {"code": "FR.INR.RINR",      "unit": "%",     "name": "Real Interest Rate (%)"},
    "current_account":{"code": "BN.CAB.XOKA.GD.ZS","unit": "% GDP","name": "Current Account Balance (% GDP)"},
}

COUNTRY_CODES = {
    "US": "US", "IN": "IN", "UK": "GB",
    "DE": "DE", "JP": "JP", "CN": "CN",
}

BASE_URL = "https://api.worldbank.org/v2"


async def fetch_indicator(indicator_key: str, country: str = "US", years: int = 10) -> List[Dict[str, Any]]:
    """Fetch historical data for a given indicator from the World Bank API."""
    meta = WB_INDICATORS.get(indicator_key)
    if not meta:
        raise ValueError(f"Unknown indicator '{indicator_key}'. Valid: {list(WB_INDICATORS.keys())}")

    country_code = COUNTRY_CODES.get(country.upper(), country)
    url = f"{BASE_URL}/country/{country_code}/indicator/{meta['code']}"

    params = {
        "format": "json",
        "per_page": years,
        "mrv": years,       # most recent values
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = client.get(url, params=params)  # type: ignore
        # httpx sync inside async for simplicity; swap to await for production
        import httpx as _httpx
        response = _httpx.get(url, params=params, timeout=15.0)
        response.raise_for_status()
        raw = response.json()

    if not raw or len(raw) < 2 or not raw[1]:
        return []

    records = []
    for entry in raw[1]:
        if entry.get("value") is None:
            continue
        records.append({
            "indicator": indicator_key,
            "country": country.upper(),
            "value": float(entry["value"]),
            "period": str(entry["date"]),
            "unit": meta["unit"],
            "source": "World Bank Open Data",
        })

    return records


def get_supported_indicators() -> Dict[str, Any]:
    return {
        key: {"name": val["name"], "unit": val["unit"]}
        for key, val in WB_INDICATORS.items()
    }
