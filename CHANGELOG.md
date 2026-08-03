# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.1] - 2026-08-03

### Fixed
- HACS validation workflow now uses the maintained `hacs/action`, fixing the
  failing release pipeline.

## [0.2.0] - 2026-08-03

### Added
- Repository documentation files: `LICENSE`, `SECURITY.md`, `SUPPORT.md`,
  `CONTRIBUTING.md`, `CHANGELOG.md`, `THIRD_PARTY_NOTICES.md`.
- GitHub Actions workflows for HACS validation, Hassfest validation, Python
  linting, and dependency review.
- `codeowners` field added to `manifest.json`.
- Diagnostics support, with the access token redacted from the output.

### Changed
- Improved credential handling: the access token now uses a password-masked
  field in the config flow; bearer tokens are redacted from log messages and
  error output.
- Updated `README.md` with expanded documentation sections.

### Security
- Bearer tokens are redacted from error messages and log output, and the access
  token is redacted from diagnostics output.
- Server URLs are validated: plain HTTP is rejected for anything other than
  loopback or private-network addresses.

### Breaking
- An entry configured with a plain-HTTP URL pointing at a public host no longer
  loads, and reports a configuration error until the URL is changed to HTTPS.

## [0.1.5] - 2026-08-03

### Changed
- Polling interval reduced to 10 seconds for faster state updates.

## [0.1.4] - 2026-08-03

### Added
- Text and timestamp sensor support.
- Automatic pruning of entities when datastreams are removed from the device
  template.

### Fixed
- Entity registry cleanup for removed datastreams.

## [0.1.3] - 2026-07-28

### Added
- Brand icon and logo assets.

## [0.1.2] - 2026-07-28

### Changed
- Manifest version bump.

## [0.1.1] - 2026-07-28

### Added
- Request timeout handling for API calls.

### Fixed
- Timeout handling to prevent overlapping polls.

## [0.1.0] - 2026-07-28

### Added
- Initial integration release.
- Device discovery and configuration via config flow.
- Platform support: `sensor`, `binary_sensor`, `switch`, `number`, `select`.
- Token-based authentication with reauthentication flow.
- Coordinator-based polling for state updates.

[Unreleased]: https://github.com/intelliThings-official/home-assistant-intellithings/compare/0.2.1...HEAD
[0.2.1]: https://github.com/intelliThings-official/home-assistant-intellithings/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/intelliThings-official/home-assistant-intellithings/compare/0.1.5...0.2.0
[0.1.5]: https://github.com/intelliThings-official/home-assistant-intellithings/compare/0.1.4...0.1.5
[0.1.4]: https://github.com/intelliThings-official/home-assistant-intellithings/compare/0.1.3...0.1.4
[0.1.3]: https://github.com/intelliThings-official/home-assistant-intellithings/compare/0.1.2...0.1.3
[0.1.2]: https://github.com/intelliThings-official/home-assistant-intellithings/compare/0.1.1...0.1.2
[0.1.1]: https://github.com/intelliThings-official/home-assistant-intellithings/compare/0.1.0...0.1.1
[0.1.0]: https://github.com/intelliThings-official/home-assistant-intellithings/releases/tag/0.1.0