"""Constants shared across the IntelliThings integration."""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "intellithings"

CONF_BASE_URL = "base_url"
CONF_TOKEN = "token"

# The platform is cloud-polled over HTTP. 10s so a value changed elsewhere — the
# mobile app, a workflow, a schedule — shows up promptly.
#
# The binding limit is not the 120/min per token this uses 6 of, it is the
# 300/min per IP: every device in one Home Assistant instance shares that
# instance's address, so this caps a single instance at ~50 devices. Anyone
# running more should disable polling in the entry's system options and drive
# homeassistant.update_entity from an automation at whatever rate suits them.
UPDATE_INTERVAL = timedelta(seconds=10)

# Hard ceiling on a single request. Must stay under UPDATE_INTERVAL so a stalled
# request is abandoned before the next poll is due — otherwise polls overlap and
# the coordinator sits blocked, leaving entities showing a stale value instead of
# going unavailable.
REQUEST_TIMEOUT = 8

API_PREFIX = "/api/ha/v1"
