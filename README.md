
# Boffer Bot — Rules Assistant ✅

Short Discord bot that answers rule-related questions about Dagorhir and Hearthlight using the Gemini API. It listens for messages that begin with `!rulescheck` and replies with concise answers (optionally referencing uploaded rule documents).

---

## 🔧 Requirements

- Python 3.14+
- A virtual environment (recommended)
- A Gemini API key (set `GEMINI_API_KEY` in your `.env`)
- A Discord Bot Token (set `DISCORD_TOKEN` in your `.env`)

Install project dependencies with uv (or pip if you prefer):

```bash
uv sync
```

## ⚙️ Environment

Create a `.env` file in the project root with:

```env
DISCORD_TOKEN=your_discord_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

## ▶️ Run the bot

Start the bot locally:

```bash
uv run main.py
```

Once running, send a message in a server where the bot is present:

```
!rulescheck tell me about dagorhir
```

The bot will send a concise response and may reference the local files in `rules/` if they are uploaded/configured.

## 📂 Rules files

Place rulebook files in the `rules/` folder. Current recognized files include:

- `rules/DagorhirManualofArms.pdf`
- `rules/HearthlightRulebook.pdf`

The bot can upload these to Gemini's File Search (or use them as context) to provide grounded answers.

## 🐳 Docker deployment

You can build and run the bot in Docker. The repository includes a `dockerfile` at the project root — specify it explicitly if needed.

Create a `.env` in the project root containing at least the required variables:

```env
DISCORD_TOKEN=your_discord_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

Build the Docker image:

```bash
docker build -t boffer-bot -f dockerfile .
```

Run the container (mount the `rules/` folder so the bot can access local rule files):

Linux / macOS / WSL:

```bash
docker run --env-file .env -v "$(pwd)/rules:/app/rules" --name boffer-bot --rm -it boffer-bot
```

Windows PowerShell:

```powershell
docker run --env-file .env -v ${PWD}/rules:/app/rules --name boffer-bot --rm -it boffer-bot
```

Run detached (background):

```bash
docker run --env-file .env -v "$(pwd)/rules:/app/rules" --name boffer-bot -d boffer-bot
```

If you change code, rebuild the image:

```bash
docker build -t boffer-bot -f dockerfile .
```

**Notes:**

- The container does not expose network ports; it connects to Discord via the bot token.
- Ensure `.env` contains `DISCORD_TOKEN` and `GEMINI_API_KEY` so the bot can authenticate.

## ⚠️ Notes & Troubleshooting

- Discord requires the `message_content` intent to read message content. Enable it in the Developer Portal and set `intents.message_content = True` in `main.py` (already present). Privileged intents must be enabled for your bot in the portal.
- If you get a 401 Unauthorized when the bot starts, check `DISCORD_TOKEN` in `.env`.
- Gemini-related behaviour depends on the installed `google-generativeai` version — if File Search features are missing, the bot will fall back to model-only responses.

---

