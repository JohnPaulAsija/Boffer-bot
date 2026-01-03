# bot.py
import os

import discord
from dotenv import load_dotenv
from goog import generate_response
from pathlib import Path
from goog import init_ai_client

load_dotenv()
# Initialize AI client and system instructions
ai_client, SYSTEM_INSTRUCTION, rules_file_refs = init_ai_client()

# Retrieve the Discord API token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    print("ERROR: DISCORD_TOKEN not found in .env file")
    exit(1)
print(f"Using DISCORD_TOKEN: {TOKEN}")

# Set up Discord client with message content intent
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Get the absolute path of the current file
current_file_path = os.path.realpath(__file__)
print(f"Absolute path of current file: {current_file_path}")

# Get the directory containing the current file
current_directory = os.path.dirname(current_file_path)

# Read the status message from status_message.txt
status_message_path = Path(current_directory) / "status_message.txt"
status_message = status_message_path.read_text(encoding="utf-8")

# Discord event handlers
# Event: on_ready (bot has connected to Discord)
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    # Send a startup message to a channel in each guild (only once)
    if getattr(client, "_startup_notified", False):
        return
    for guild in client.guilds:
        try:
            # Prefer the guild's system channel if the bot can send messages there
            channel = guild.system_channel
            if channel is None or not channel.permissions_for(guild.me).send_messages:
                # Otherwise find the first text channel where the bot can send messages
                channel = next(
                    (c for c in guild.text_channels if c.permissions_for(guild.me).send_messages),
                    None,
                )

            if channel is None:
                print(f"No sendable channel found in guild {guild.name} ({guild.id})")
                continue

            await channel.send(status_message)
            print(f"Sent startup message to {guild.name}#{channel.name}")
        except Exception as e:
            print(f"Error sending startup message to {guild.name} ({guild.id}): {e}")

    client._startup_notified = True

# Event: on_message (bot receives a message / a user interacts with the bot)
@client.event
async def on_message(message):
    if message.content.lower().startswith('!rulescheck'):
        prompt = message.content[11:].strip()
        print(f"{message.author}: {message.content}")
        print(f"Prompt: {prompt}")
        
        response = generate_response(prompt, client=ai_client, system_instructions=SYSTEM_INSTRUCTION, rules_file_refs=rules_file_refs)
        
        # Split response into chunks of 1000 characters to fit Discord's limit
        for i in range(0, len(response), 1000):
            chunk = response[i:i+1000]
            await message.channel.send(chunk)

    if message.content.lower().startswith('!about'):
        await message.channel.send(status_message)

client.run(TOKEN)
