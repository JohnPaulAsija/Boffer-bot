# Boffer Bot

Boffer Bot is a Discord bot that answers Dagorhir and Hearthlight LARP rules questions using
Google Gemini 2.5 Flash. It uploads PDF rulebooks from `rules/` to Gemini at startup, then
responds to `!rulescheck` messages with cited, grounded answers. The codebase is intentionally
minimal — two main modules (`main.py`, `goog.py`) and one test file.

---

## Commands

| Purpose | Command |
|---|---|
| Run bot locally | `uv run main.py` |
| Run tests | `uv run pytest` |
| Install / sync deps | `uv sync` |
| Docker build | `docker build -t boffer-bot -f dockerfile .` |
| Docker run (Linux/macOS) | `docker run --env-file .env -v "$(pwd)/rules:/app/rules" --name boffer-bot --rm -it boffer-bot` |
| Docker run (PowerShell) | `docker run --env-file .env -v ${PWD}/rules:/app/rules --name boffer-bot --rm -it boffer-bot` |
| Docker run detached | `docker run --env-file .env -v "$(pwd)/rules:/app/rules" --name boffer-bot -d boffer-bot` |

**Environment:** Requires `.env` with `DISCORD_TOKEN` and `GEMINI_API_KEY`.

---

## Guardrails

- **Never commit or push** without explicit user instruction.
- **Never modify `system_instructions.txt`** without explicit confirmation — AI behavior changes
  are deliberate and reviewed.
- **Never use `pip`** — always use `uv` for all dependency operations.
- **Never claim a task is done** without running `uv run pytest` first and confirming tests pass.

---

## Architecture

- **`goog.py`** owns all Gemini API logic: client initialization, PDF file upload, content
  building, and API calls.
- **`main.py`** owns Discord events: `on_ready`, `on_message`, and command routing.
- PDF rulebooks are uploaded to Gemini at startup; file references are cached in memory for
  the bot's lifetime.
- Responses are chunked at 1000 characters to stay under Discord's 2000-character message limit.

---

## Domain Notes

- Bot commands: `!rulescheck <question>` and `!about`.
- Rulebooks live in `rules/` — be aware of Gemini file upload caching before modifying PDFs.
- `system_instructions.txt` governs AI behavior — treat changes here like config changes,
  not code changes. Changes require explicit user confirmation.
