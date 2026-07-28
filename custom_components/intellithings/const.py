"""Constants shared across the IntelliThings integration."""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "intellithings"

CONF_BASE_URL = "base_url"
CONF_TOKEN = "token"

# The platform is cloud-polled over HTTP. 30s keeps entities responsive without
# hammering the API; the backend rate limit allows 120 requests/min per token,
# so there is ample room for user-driven commands on top of this.
UPDATE_INTERVAL = timedelta(seconds=30)

# Hard ceiling on a single request. Comfortably under UPDATE_INTERVAL so a stalled
# request is abandoned before the next poll is due — without one, aiohttp would
# wait minutes and the coordinator would sit blocked, leaving entities showing a
# stale value instead of going unavailable.
REQUEST_TIMEOUT = 15

API_PREFIX = "/api/ha/v1"
