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
