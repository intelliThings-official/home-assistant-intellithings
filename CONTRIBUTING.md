# Contributing to IntelliThings for Home Assistant

Thank you for considering contributing to this project. Please take a moment to
review the guidelines below.

## Development setup

1. Clone the repository:
   ```bash
   git clone https://github.com/intelliThings-official/home-assistant-intellithings.git
   cd home-assistant-intellithings
   ```

2. Ensure you have Python 3.12 or later available.

3. Install development dependencies:
   ```bash
   pip install ruff
   ```

4. Run the utility self-check to verify your environment:
   ```bash
   python test_util.py
   ```

## Code style

- This project follows the Python style conventions enforced by
  [Ruff](https://docs.astral.sh/ruff/).
- Run Ruff before submitting a pull request:
  ```bash
  ruff check custom_components/intellithings/ test_util.py
  ```
- Keep platform files small. Shared logic belongs in `entity.py` or the
  coordinator.
- Use descriptive variable names. Comments should explain *why*, not *what*.
- Follow the existing patterns for entity platforms, config flow, and API
  interaction.

## Testing requirements

- Run `test_util.py` to verify value-coercion helpers:
  ```bash
  python test_util.py
  ```
- If you add new utility functions, add corresponding test cases to
  `test_util.py`.
- If you add new platforms or modify entity behaviour, test manually in a
  Home Assistant development instance.

## Pull-request expectations

- Each pull request should address a single concern. If you have multiple
  changes, submit separate pull requests.
- Provide a clear description of the change, why it is needed, and how it was
  tested.
- Ensure all existing tests pass.
- Add or update documentation in `README.md` if the change affects the user
  interface or configuration.
- Keep backward compatibility in mind. Breaking changes should be clearly
  documented in both the pull request and the release notes.

## Reporting bugs

Open an issue on the [GitHub issue tracker](https://github.com/intelliThings-official/home-assistant-intellithings/issues)
with:

- A clear, descriptive title.
- Steps to reproduce the issue.
- The integration version and Home Assistant version you are using.
- Relevant logs (redacted of any personal or sensitive data).
- What you expected to happen and what actually happened.

## Submitting feature requests

Open an issue on the [GitHub issue tracker](https://github.com/intelliThings-official/home-assistant-intellithings/issues)
with:

- A clear description of the feature you would like to see.
- Why it would be useful and how you envision it working.
- Any relevant examples from other integrations.

## Security reporting

**Do not report security vulnerabilities through public GitHub issues.** See
[`SECURITY.md`](SECURITY.md) for the private reporting process.

## Licensing

By contributing to this repository, you agree that your contributions will be
licensed under the Apache License, Version 2.0. You represent that you have the
right to license the contributed code and assets under this licence.

Do not submit code or assets that you do not have the right to distribute or
that are incompatible with the Apache License, Version 2.0.