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

client = commands.Bot(command_prefix="!", description="Meme Machine")


@client.event
async def on_ready():
    print("Logged in as\n"
          "{}\n"
          "{}\n"
          "---".format(client.user.name, client.user.id))


@client.command()
async def echo():
	await client.say('Echo')
	
@client.command()
async def encounter():
    p = pokemon.getRandomPokemon(-1)
    # name = pokemon.name
    encounter_msg = "A wild " + p + " appears."
    await client.say(encounter_msg)

'''
@client.command()
async def join():
	voice = sounds.JoinVoiceChannel(client)
'''

# logs in the client and runs the bot using token read in from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

login_token = (config["token"])
client.login()
client.run(login_token)
