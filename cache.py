"""
Simple TTL cache. Replace the in-memory store with Redis by swapping the
get/set methods to use `redis.Redis` — the interface stays identical.

  import redis
  r = redis.Redis(host="localhost", port=6379, decode_responses=True)
  r.setex(key, ttl, json.dumps(value))
  cached = r.get(key)
"""

import time
import json
from typing import Any, Optional

_store: dict = {}   # { key: (value, expires_at) }

DEFAULT_TTL = 3600  # 1 hour


def cache_get(key: str) -> Optional[Any]:
    entry = _store.get(key)
    if not entry:
        return None
    value, expires_at = entry
    if time.time() > expires_at:
        del _store[key]
        return None
    return value


def cache_set(key: str, value: Any, ttl: int = DEFAULT_TTL) -> None:
    _store[key] = (value, time.time() + ttl)


def cache_delete(key: str) -> None:
    _store.pop(key, None)


def cache_stats() -> dict:
    now = time.time()
    active = {k: v for k, v in _store.items() if v[1] > now}
    return {"active_keys": len(active), "keys": list(active.keys())}
