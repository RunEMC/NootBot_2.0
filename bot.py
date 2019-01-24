import os
import sys
import discord
import logging
import asyncio
from discord.ext import commands
import json
# import sounds
# import pokemon

# Logging/Debugging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Create new client
client = discord.Client()

# Global flag variables
isBotReady = False

# Handle on ready events
@client.event
async def on_ready():
    global isBotReady
    isBotReady = True
    print("Bot ready!")

# Handle on message events
@client.event
async def on_message(message):
    msgContents = message.content
    msgChannel = message.channel
    msgAuthor = message.author

    # Ensure that the message is using Pybot Commands
    if msgContents.startswith('!') and isBotReady:
        # Get command
        commandArray = msgContents.split(" ")
        command = commandArray[0][1:]

        # ~~~~~ Process command ~~~~~ #
        # Basic commands
        if command == "help":
            await client.send_message(msgChannel, "I can't help you right now.")

        elif command == "die":
            if msgAuthor.id == "171429655008509954": # You can set this to your own id
                await client.send_message(msgChannel, "Ok, goodbye!")
                await client.logout()
            else:
                await client.send_message(msgChannel, "Sorry, only RunEMC can do that!")

        elif command == "getid":
            await client.send_message(msgChannel, msgAuthor.id)

        # Default
        else:
            print(msgAuthor.id)
            await client.send_message(msgChannel, "Unrecognized command: " + msgContents)

    elif not isBotReady:
        await client.send_message(msgChannel, "Sorry, I'm still starting up, please wait")


# Logs in the client and runs the bot using token read in from config.json
# Client is logged in at the end since run() is blocking
with open('config.json') as config_file:
    config = json.load(config_file)

client.run(config["token"])