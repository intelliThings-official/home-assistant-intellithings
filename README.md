# IntelliThings for Home Assistant

Adds IntelliThings devices to Home Assistant as native entities — sensors that
graph, switches that toggle, setpoints you can change.

One config entry per device. The device's exposed datastreams become entities;
which ones, and what type each is, is decided in IntelliThings on the device
template, so adding an entity does not need a new release of this integration.

## Requirements

- The **Home Assistant** plugin enabled for your organisation (Plugins page,
  organisation admin or moderator).
- At least one datastream mapped to a Home Assistant entity type on the device
  template's **Datastreams** tab.
- An access token generated from the device's detail page.

## Install

**HACS** — HACS → Integrations → ⋮ → Custom repositories → add this repository as
an *Integration* → install **IntelliThings** → restart Home Assistant.

**Manual** — copy `custom_components/intellithings` into your Home Assistant
`config/custom_components/` directory and restart.

## Set up

Settings → Devices & Services → **Add Integration** → **IntelliThings**, then
paste the server URL and access token shown when you generated the token.

Repeat per device — each token covers exactly one device.

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

## Behaviour

- State is polled every 30 seconds. Commands are sent immediately and followed by
  a refresh, because the platform normalises values and may reject one.
- Changing which datastreams are exposed — or their entity type, bounds or
  options — is picked up automatically within one poll. The integration reloads
  itself and rebuilds its entities; names, areas and history survive it.
- Entities show as unavailable when the device is offline, rather than showing
  the last known reading.
- Revoking the token, or switching the plugin off for the organisation, cuts
  access within one poll. Home Assistant then asks you to re-authenticate; paste
  a freshly generated token to reconnect.

## Not yet supported

`climate`, `cover` and `light` entities bundle several datastreams into one
entity, which needs a mapping UI on the device template rather than a per-datastream
toggle. A thermostat works today as a `number` plus a `select`.

## Development

This lives in the IntelliThings monorepo under `home-assistant/` and is mirrored
to a public repository for HACS. Run the value-coercion self-check with:

```
python3 home-assistant/test_util.py
```
