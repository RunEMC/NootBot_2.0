import os
import sys
import discord
import logging
import asyncio
from discord.ext import commands

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
    await bot.say('Echo')

	
# Simple client login and starting the bot.
login_token = ('MTc3MTc3ODgwNjkyOTE2MjI1.C103MA.sp3U_F2IBgtf6yKCLu2x7tWET-M')
client.login()
client.run(login_token)