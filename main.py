import discord
import os
from mcstatus import MinecraftServer

from skingrabber import skingrabber
from mojang import MojangAPI
sg = skingrabber()
client = discord.Client(activity=discord.Game(name='stuff'))
ClientToken = os.environ['Token']

async def GetPlayer(message):
 mess = message.content
 Player = mess[mess.index(" ")+1:]
 uuid = MojangAPI.get_uuid(Player)
 try:
  profile = MojangAPI.get_profile(uuid)
  response = "https://crafatar.com/renders/body/" + uuid
  await message.reply(response,mention_author=False)
  
 except:
  await message.reply("nope")


@client.event
async def on_ready():
  print("Logged in as {0.user}".format(client))
  


@client.event
async def on_message(message):
 if message.author == client.user:
    return
 if message.content.startswith("!player "):
    await GetPlayer(message)

client.run(ClientToken)