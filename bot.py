import os
import sys
import discord
import logging
import asyncio
from discord.ext import commands
import json
# import sounds
import pokemon

# Logging/Debugging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Create new client
client = discord.Client()

@client.event
async def on_message(message):
    msgContents = message.content
    msgChannel = message.channel

    # Ensure that the message is using Pybot Commands
    if msgContents.startswith('!'):
        # Get command
        commandArray = msgContents.split(" ")
        command = commandArray[0][1:]

        # ~~~~~ Process command ~~~~~ #
        # Basic commands
        if command == "help":
            await client.send_message(msgChannel, "I can't help you right now.")

        elif command == "die":
            await client.send_message(msgChannel, "Ok, goodbye!")
            await client.logout()

        else:
            await client.send_message(msgChannel, "Unrecognized command: " + msgContents)


# Logs in the client and runs the bot using token read in from config.json
# Client is logged in at the end since run() is blocking
with open('config.json') as config_file:
    config = json.load(config_file)

client.run(config["token"])