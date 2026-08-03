# IntelliThings for Home Assistant

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

Adds IntelliThings devices to Home Assistant as native entities — sensors that
graph, switches that toggle, setpoints you can change.

One config entry per device. The device's exposed datastreams become entities;
which ones, and what type each is, is decided in IntelliThings on the device
template, so adding an entity does not need a new release of this integration.

---

## About

IntelliThings for Home Assistant bridges IntelliThings IoT devices into Home
Assistant. Each device is configured as its own integration entry, using a
per-device access token. The device template defines which datastreams are
exposed and what Home Assistant entity type each becomes. Changes to the
template are picked up automatically without requiring a new release of this
integration.

The integration communicates with the IntelliThings cloud service using the
device access token you provide.

---

## Installation

### Via HACS (recommended)

1. Ensure [HACS](https://hacs.xyz) is installed in your Home Assistant instance.
2. In HACS, go to **Integrations**.
3. Click the **⋮** menu (three dots) in the top-right corner and select
   **Custom repositories**.
4. Add this repository URL:
   `https://github.com/intelliThings-official/home-assistant-intellithings`
   and select **Integration** as the category.
5. Click **Add**.
6. The **IntelliThings** integration should now appear in HACS. Click **Install**.
7. Restart Home Assistant.

### Manual

Copy the `custom_components/intellithings` directory into your Home Assistant
`config/custom_components/` directory and restart.

---

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**.
2. Search for **IntelliThings**.
3. Enter the **Server URL** and **Access token** shown when you generated the
   token from the device.
4. Repeat per device — each token covers exactly one device.

The server URL must use **HTTPS**. Plain `http://` is accepted only for loopback
and private-network addresses (`localhost`, `127.0.0.1`, `10.x`, `172.16–31.x`,
`192.168.x`, `*.local`, `*.lan`), where TLS is often unavailable.

### Reauthentication

If a token is revoked or the Home Assistant plugin is switched off for your
organisation, the integration will prompt you to re-authenticate. Generate a new
token from the device detail page and paste it into the reauthentication dialog.

---

## Updating

- Updates are delivered through versioned HACS / GitHub releases.
- Before updating, review the [release notes](https://github.com/intelliThings-official/home-assistant-intellithings/releases)
  for any breaking changes or new features.
- Home Assistant normally requires a manual restart after updating a custom
  integration.
- The integration **must not** silently download or replace its own source code.
  All updates must go through HACS or a manual file replacement.
- Users may create their own opt-in Home Assistant automation for update
  installation and restart, but unattended updates are not enabled by this
  integration.

---

## Entity types

Set per datastream in IntelliThings. Access level is shared with the member
workflow setting: **Hidden** datastreams are never exposed, and the writable
types need **Full access**.

| IntelliThings | Home Assistant | Writable |
|---|---|---|
| Sensor | `sensor` | no |
| Binary sensor | `binary_sensor` | no |
| Switch | `switch` | yes |
| Number | `number` | yes |
| Select | `select` | yes |

Set a **device class** on readings (`temperature`, `humidity`, `power`, …) —
Home Assistant uses it for the icon and units. Add a **state class** of
`measurement` (or `total_increasing` for meters) if you want long-term
statistics and energy-style charts.

---

## Behaviour

- State is polled every 10 seconds. Commands are sent immediately and followed by
  a refresh, because the platform normalises values and may reject one.
- The API allows 300 requests a minute per IP address, and every device in one
  Home Assistant instance shares that address — so roughly **50 devices per
  instance** at the default rate. Past that, turn off *Enable polling for
  updates* in the entry's system options and call `homeassistant.update_entity`
  from an automation at an interval that suits your fleet.
- Changing which datastreams are exposed — or their entity type, bounds or
  options — is picked up automatically within one poll. The integration reloads
  itself and rebuilds its entities; names, areas and history survive it.
  Datastreams that stop being exposed are removed from Home Assistant.
- Entities show as unavailable when the device is offline, rather than showing
  the last known reading.
- Revoking the token, or switching the plugin off for the organisation, cuts
  access within one poll. Home Assistant then asks you to re-authenticate; paste
  a freshly generated token to reconnect.

---

## Supported versions

| Component | Minimum version |
|---|---|
| Home Assistant | 2024.11.0 |
| Integration | Latest GitHub release |

The minimum Home Assistant version is defined in [`hacs.json`](hacs.json) and
may increase in future releases.

---

## Security

See [`SECURITY.md`](SECURITY.md) for supported versions, how to report
vulnerabilities, and credential-exposure guidance.

---

## Support

See [`SUPPORT.md`](SUPPORT.md) for where to get help, report bugs, and submit
feature requests.

---

## Privacy

See the [myCistern terms and conditions](https://mycistern.com/terms-and-conditions/).

At a high level, this integration:

- Communicates with the IntelliThings service using the device access token that
  you provide, over the server URL you configure.
- Sends and receives device identifiers, device state, and the commands you
  issue from Home Assistant.
- Writes the server URL, HTTP status codes and server error text to the Home
  Assistant log when a request fails. Access tokens are redacted from that
  output, and are never included in diagnostics downloads.
- Sends no data anywhere other than the server URL you configure. There is no
  telemetry, analytics, or third-party reporting.

For full details on how your data is collected, used, and retained, refer to the
document linked above.

---

## Safety notice

This integration is **not** intended to be the sole control mechanism for
safety-critical systems, including but not limited to:

- Fire, smoke, or gas detection and protection.
- Medical or life-support equipment.
- Emergency notification or response systems.
- Access-control or physical security systems.
- Industrial machinery or processes.
- Equipment where a failure could reasonably be expected to cause injury or
  material damage.

Always ensure that redundant and fail-safe mechanisms are in place for any
application where the unavailability, misconfiguration, or unexpected behaviour
of this integration could lead to harm or loss.

---

## Non-affiliation notice

IntelliThings for Home Assistant is an independent custom integration maintained
by IntelliThings. It is not endorsed, certified, maintained, or supported by the
Home Assistant project, HACS, or the Open Home Foundation.

---

## Licence

Copyright 2026 myCistern Operations GmbH.

The source code in this repository is licensed under the Apache License,
Version 2.0. See the [`LICENSE`](LICENSE) file for the full text. "Home
Assistant" is a trademark of the Open Home Foundation, used here only to
describe compatibility.

---

## Not yet supported

`climate`, `cover` and `light` entities bundle several datastreams into one
entity, which needs a mapping UI on the device template rather than a
per-datastream toggle. A thermostat works today as a `number` plus a `select`.

---

## Development

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for development setup, code style, and
pull-request guidelines.

Run the value-coercion self-check with:

```
python3 test_util.py
```
