import os
import discord
import asyncio
from discord.ext import commands


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


# Simple client login and starting the bot.
client.run("MTc3MTc3ODgwNjkyOTE2MjI1.C103MA.sp3U_F2IBgtf6yKCLu2x7tWET-M")
