# Repository Guidelines

## Project Structure & Module Organization
- `ytpodcast/` contains the FastAPI application, organized by layer:
  - `api.py` app entrypoint and routes registration.
  - `controller/` request handlers and response mapping.
  - `service/` business logic.
  - `client/` external API clients (YouTube API, yt-dl).
  - `model/` DTOs and mappers grouped by layer.
  - `config/` and `container/` for configuration and dependency wiring.
- Root files: `requirements.txt` for dependencies, `README.md` for a short overview.
- There are currently no `tests/` or fixtures directories.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate` create and activate a virtualenv.
- `pip install -r requirements.txt` install runtime dependencies.
- `python -m ytpodcast.api` run the API using the built-in `uvicorn` launcher.
- `uvicorn ytpodcast.api:app --host 0.0.0.0 --port 8459` run explicitly via Uvicorn.

## Configuration & Environment
- Environment variables are loaded via `python-dotenv` in `ytpodcast/container/default_container.py`.
- Common settings: `APP_NAME`, `DEBUG`, `API_HOST`, `API_PORT`, `YT_API_BASE_URL`, `YT_API_KEY`, `YTDL_DEFAULT_FORMAT`.
- Example: `export YT_API_KEY=...` before running the API.

## Coding Style & Naming Conventions
- Python code uses 4-space indentation and PEP 8 conventions.
- Use `snake_case` for modules/functions, `PascalCase` for classes, and `UPPER_SNAKE_CASE` for constants.
- Keep layers separated (controller → service → client/model) to match existing structure.
- Pylance/Pyright uses strict type checking; add explicit types for parameters, returns, and variables.
- Add docstrings for functions and methods to satisfy pylint C0116.
- Add module docstrings and resolve pylint warnings (naming, too-few-public-methods, duplicate-code) for new or changed modules.
- Pylint configuration: `.pylintrc` disables `invalid-name`.
- Naming conventions:
  - Controller models describe response payloads (e.g., `GetChannelResponse`, `GetChannelXmlResponse`).
  - Client models describe what a client method returns (e.g., `VideoResponse`, `ChannelResponse`).
  - Service models describe the domain (`Video`, `Channel`).
  - Mapper names describe the model they build (e.g., `GetChannelResponseMapper.create_from_channel`, `VideoMapper.create_from_video_response`).
  - Avoid `Model` in class names.

## Testing Guidelines
- No test framework is configured yet.
- If adding tests, place them under `tests/` and name files `test_*.py`.
- Document new test commands in this file when introduced.

## Commit & Pull Request Guidelines
- Commit messages in history are short, sentence-case summaries (e.g., "Initial implementation ...").
- PRs should include a clear description, reproduction or test steps, and any config changes.

## Agent-Specific Notes
- Keep changes minimal and consistent with the existing layered architecture.
