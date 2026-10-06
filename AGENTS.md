# Repository Guidelines

## Project Structure & Module Organization

This Python 3.12+ Telegram bot checks message characters and warns about unsupported letters. `bot.py` handles Telegram polling, messages, captions, and quoted text. `bot_logic.py` contains pure Unicode validation functions; keep detection rules separate from Telegram integration. `tests/test_bot_logic.py` covers character rules, and `tests/test_bot.py` covers asynchronous replies. `cat_avatar.jpg` is the bot avatar. Runtime and deployment files are `requirements.txt`, `Dockerfile`, `docker-compose.yml`, and `deploy.sh`; usage documentation lives in `readme.md`.

## Build, Test, and Development Commands

- `python3 -m venv .venv && source .venv/bin/activate`: create and activate a virtual environment using Python 3.12+.
- `pip install -r requirements.txt`: install pinned dependencies.
- `python bot.py`: start local Telegram polling after configuring `BOT_TOKEN` in `.env`.
- `python -m unittest discover -s tests`: run the complete test suite.
- `docker build -t telegram-language-bot .`: build the image; unit tests must pass during the build.
- `docker compose up -d --build`: build and start the bot in the background.
- `docker compose logs -f`: follow container logs.

## Coding Style & Naming Conventions

Use four-space indentation, `snake_case` functions and variables, `UPPER_SNAKE_CASE` constants, and descriptive `PascalCase` test classes. Follow existing type hints in pure logic, including `str | None`. Keep handlers asynchronous and detection functions independently testable. No formatter or linter is configured; follow surrounding style and avoid unrelated formatting changes.

## Testing Guidelines

Tests use standard-library `unittest`, `IsolatedAsyncioTestCase`, and `AsyncMock`; no numeric coverage threshold is configured. Name files `test_*.py` and methods `test_<expected_behavior>`. Add regression cases for changed detection rules or message handling. Cover ASCII and Georgian letters, unsupported scripts and accented Latin letters, NFC normalization, emoji, empty/short input, captions, and quotes as relevant. Mock Telegram replies instead of making network calls.

## Commit & Pull Request Guidelines

History uses short, descriptive subjects with optional component prefixes, such as `bot: check language in photo caption` or `deploy: add deploy script, upd readme`. Follow that pattern and keep commits focused. PRs should describe the behavior change, include representative input/output examples and test results, and link related issues when applicable. Update `readme.md` when user-facing behavior or setup changes.

## Security & Configuration

Keep bot tokens and SSH credentials out of commits. Use local `.env` and `.env.deploy` files; `.env.deploy.example` documents deployment settings. `./deploy.sh` updates the configured remote checkout and rebuilds its running container, so run it only for an intended deployment.
