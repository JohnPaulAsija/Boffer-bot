
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

## ⚠️ Notes & Troubleshooting

- Discord requires the `message_content` intent to read message content. Enable it in the Developer Portal and set `intents.message_content = True` in `main.py` (already present). Privileged intents must be enabled for your bot in the portal.
- If you get a 401 Unauthorized when the bot starts, check `DISCORD_TOKEN` in `.env`.
- Gemini-related behaviour depends on the installed `google-generativeai` version — if File Search features are missing, the bot will fall back to model-only responses.

---

