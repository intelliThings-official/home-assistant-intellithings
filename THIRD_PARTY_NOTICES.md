# Third-Party Notices

No third-party code, icons, fonts, or other assets are copied into or vendored
within this repository. The brand images in `custom_components/intellithings/brand/`
are IntelliThings' own artwork. Everything else is either original code or a call
into Home Assistant and the Python standard library.

At runtime the integration relies on the following, all of which ship with Home
Assistant and none of which are redistributed here:

- **Home Assistant** — the core platform on which this integration runs.
  Apache-2.0. <https://github.com/home-assistant/core>
- **aiohttp** — HTTP communication with the IntelliThings platform.
  Apache-2.0. <https://github.com/aio-libs/aiohttp>
- **voluptuous** — configuration validation in the config flow.
  BSD-3-Clause. <https://github.com/alecthomas/voluptuous>

---

**Maintainers:** This file must be updated whenever third-party material (code,
libraries, icons, fonts, or other assets) is added to the repository. Each entry
should include the component name, source URL, licence, and a brief description
of how the component is used.