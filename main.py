# bot.py
import os

import discord
from dotenv import load_dotenv
from goog import generate_response

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    print("ERROR: DISCORD_TOKEN not found in .env file")
    exit(1)
print(f"Using DISCORD_TOKEN: {TOKEN}")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    # Send a startup message to a channel in each guild (only once)
    if getattr(client, "_startup_notified", False):
        return

    status_message = "Boffer Bot is now online!"

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

@client.event
async def on_message(message):
    if message.content.lower().startswith('!rulescheck'):
        prompt = message.content[11:].strip()
        print(f"{message.author}: {message.content}")
        print(f"Prompt: {prompt}")
        
        response = generate_response(prompt)
        
        # Split response into chunks of 1000 characters to fit Discord's limit
        for i in range(0, len(response), 1000):
            chunk = response[i:i+1000]
            await message.channel.send(chunk)

client.run(TOKEN)
