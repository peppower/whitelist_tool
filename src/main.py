import discord
import os
from dotenv import load_dotenv
import requests
from mcrcon import MCRcon

mojangAPI = "https://api.minecraftservices.com/minecraft/profile/lookup/name/"

load_dotenv()

DISCORD_TOKEN = str(os.getenv("DISCORD_TOKEN"))
if DISCORD_TOKEN is None:
    raise ValueError("DISCORD_TOKEN environment variable is not set")
SERVER_IP = str(os.getenv("SERVER_IP"))
if SERVER_IP is None:
    raise ValueError("SERVER_IP environment variable is not set")
RCON_PORT = int(os.getenv("RCON_PORT"))
if RCON_PORT is None:
    raise ValueError("RCON_PORT environment variable is not set")
RCON_PASSWORD = str(os.getenv("RCON_PASSWORD"))
if RCON_PASSWORD is None:
    raise ValueError("RCON_PASSWORD environment variable is not set")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # simple command trigger: "!whitelist <username>"
    if message.content.startswith("!whitelist "):
        username = message.content.split(" ", 1)[1]

        if requests.get(mojangAPI + username).status_code != 200:
            await message.channel.send('Invalid Minecraft username!')
            return

        with MCRcon(SERVER_IP, RCON_PASSWORD, RCON_PORT) as mcr:
            resp = mcr.command(f"whitelist add {username}")
        await message.channel.send(f'Added {username} to whitelist!')

client.run(DISCORD_TOKEN)
