# Security Policy

## Supported Versions

Only the latest published release of this integration receives security updates.
Older versions should be updated to the latest release before a vulnerability is
reported.

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| Older   | :x:                |

## Reporting a Vulnerability

**Do not report security vulnerabilities through public GitHub issues.**

Please report security issues privately by emailing:

**contact@mycistern.com**

We ask that you:

- Do not disclose the vulnerability publicly until a fix has been released and
  users have had a reasonable opportunity to update.
- Provide sufficient detail to allow us to reproduce and triage the issue:
  - The integration version and Home Assistant version where the issue was
    observed.
  - Steps to reproduce.
  - A description of the behaviour you expected and what actually occurred.
  - Any logs, screenshots, or proof-of-concept code, redacted of any personal
    or sensitive data.
  - Whether you believe the vulnerability is publicly known.

## What to expect

- We will acknowledge receipt of your report within a reasonable timeframe.
- We will work to validate and assess the severity of the issue.
- Response and remediation times depend on the severity and complexity of the
  vulnerability. We will provide updates as the investigation progresses.
- When a fix is ready, we will publish a new release and may disclose the
  vulnerability details after users have had time to update.

## Token or credential exposure

If your device access token or other credentials have been exposed:

1. Immediately revoke the affected token in the IntelliThings device detail
   page.
2. Generate a new token and update the integration's configuration in Home
   Assistant (the integration will prompt for reauthentication).
3. If you believe the exposed credential may have been used to access your
   device or account, notify the security contact above.

## Scope

Only the source code in this repository is covered by this policy. Issues in
Home Assistant itself, HACS, or third-party dependencies should be reported to
the respective project.