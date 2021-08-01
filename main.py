import requests
import discord
import os
import time
import math
import uuid
import tweepy
import pickle
import difflib
import asyncio
import random
from MinePI import MinePI
import iso8601
from mcstatus import MinecraftServer
from mojang import MojangAPI
import humanfriendly
import datetime
from datetime import datetime as dt
from discord.ext import tasks, commands
from discord.utils import get
from dateutil.rrule import rrule, MINUTELY
import bisect
from PIL import Image
import json
from yandex_translate import YandexTranslate



########################################### PACKAGES ABOVE

ErrorMessage = "There was an error, either fix your link or go yell at algo to fix his bot :fire:"
AttemptMessage = "Attempting to Generate MatchPost"
botstatus = "UHC"
FuturePing = None


#These are the Snowflake ID's, change per server this bot is used on
AnnouncementChannelID = 843503494564020235
DonorChannelID = 606575558997835877
LogChannelID = 843319322940407900
BotChannelID = 671568375645732874
StaffRoleID = 843981764656889866
TrialStaffRoleID = 807831001921355796
NewGameRole = "<@&863956813471547392>"


languages = {
"Azerbaijani":"az",	
"Amharic":"am",	
"English":"en",
"Arabic":	"ar",	
"Armenian":	"hy",
"Afrikaans":	"af",	
"Basque":	"eu",	
"Bashkir":	"ba",	
"Belarusian":	"be",	
"Bengal":	"bn",	
"Burmese":	"my",	
"Bulgarian":	"bg",	
"Bosnian":	"bs",
"Welsh":	"cy",
"Hungarian":	"hu",
"Vietnamese":	"vi",	
"Galician":	"gl",	
"Dutch":	"nl",	
"Greek":	"el",
"Danish":	"da",
"Hebrew":	"he",
"Yiddish":	"yi",
"Indonesian":	"id",	
"Irish":	"ga",
"Italian":	"it",
"Icelandic":	"is",	
"Spanish":	"es",	
"Chinese": "zh",	
"Korean":	"ko",
"Latvian":	"lv",
"Lithuanian":	"lt",
"Luxembourg":	"lb",	
"Malay":	"ms",
"Malayalam":	"ml",
"Maltese":	"mt",
"Macedonian":"mk",
"Mongolian":	"mn",
"German":	"de",
"Norwegian":	"no",
"Persian":	"fa",
"Polish":	"pl",
"Portuguese":	"pt",
"Romanian":	"ro",
"Russian":	"ru",
"Slovak":	"sk",
"Slovenian":	"sl",
"Thai":	"th",
"Turkish":	"tr",
"Uzbek":	"uz",
"Ukrainian":	"uk",
"Finnish":	"fi",
"French":	"fr",
"Hindi":	"hi",
"Croatian":	"hr",
"Czech":	"cs",
"Swedish":	"sv",
"Scottish":	"gd",
"Javanese":	"jv",
"Japanese":	"ja",
"Malay":	"ms",
}





client = discord.Client(activity=discord.Game(name='Do !help'))



#API KEYS
YandexToken = os.environ["YandexTranslateToken"]
ClientToken = os.environ["Token"]
ConsumerKey = os.environ["ConsumerKey"]
ConsumerSecret = os.environ["ConsumerSecret"]
AcessToken = os.environ["AcessToken"]
AcessTokenSecret = os.environ["AcessTokenSecret"]



client = discord.Client(activity=discord.Game(name='Do !help'))
translate = YandexTranslate(YandexToken)

############################################################### Don't Change above this line.



#Authenticate to Twitter
auth = tweepy.OAuthHandler(ConsumerKey, ConsumerSecret)
auth.set_access_token(AcessToken, AcessTokenSecret)

 #Create API object
api = tweepy.API(auth)
try:
 with open("UHC Bot/NoPostList.txt", "rb+") as myFile:
  NoPostList = pickle.load(myFile)
except:
  NoPostList = []


try:
 with open("UHC Bot/NoPingList.txt", "rb+") as myFile:
  NoPingList = pickle.load(myFile)
except:
  NoPingList = []  





twitterLink = "https://mobile.twitter.com/user/status/"
channel = client.get_channel(LogChannelID) 


######################################################## Auto Post Stuff
async def AnnounceGameAuto(MatchInfo,NoPost,NoPing):
  global FuturePing
  print('hello')
  MatchPost = MakePost(str(MatchInfo["id"]))
  Tags = [tag.lower() for tag in MatchInfo["tags"]]
  Content = MatchInfo["content"].replace(" ","").replace("|","").lower().replace("**","")
  #Announcing Game in Discord
  try:
   NoPost.append(str(MatchInfo["id"]))
   with open("UHC Bot/NoPostList.txt", "wb+") as myFile:
    pickle.dump(NoPost, myFile)
   channel = client.get_channel(AnnouncementChannelID)
   matchP = await channel.send(NewGameRole + MatchPost)
   await matchP.publish()
   if "nether on" in Tags or "nether enabled" in Tags or ("netherenable" in Content):
     await matchP.add_reaction("\N{FIRE}")
   if "bookshelvesenabled" in Content:
     await matchP.add_reaction("\N{BOOKS}")
  except Exception as e:
   channel = client.get_channel(LogChannelID)
   await channel.send("Errror Making Post" + str(e))

  print("second hello")
  #TWITTER
  try:
   tweet = await SendMatchPostTweet(str(MatchInfo["id"]))
   channel = client.get_channel(LogChannelID)
   await channel.send("https://mobile.twitter.com/user/status/"+str(tweet.id))
  except:
   channel = client.get_channel(LogChannelID) 
   await channel.send("Could Not Send Tweet/TweetLink")


  print("Third Hello")
  await asyncio.sleep(math.floor(30*60)) 
  print(str(NoPingList)+"helllo")
  if not (str(MatchInfo["id"]) in NoPingList):
   try:
    NoPing.append(NoPing)
    with open("UHC Bot/NoPingList.txt", "wb+") as myFile:
     pickle.dump(NoPing, myFile)
    channel = client.get_channel(AnnouncementChannelID)



    if FuturePing == None:
      Host = MatchInfo["hostingName"]
      if MatchInfo["hostingName"] == None:
        Host = MatchInfo["author"]
        
      FuturePing = " Come play a game hosted by " + Host + " on ApolloUHC"
    


    messP = await channel.send(NewGameRole + FuturePing)
    await messP.publish()
    FuturePing = None
   except Exception as e:
    channel = client.get_channel(LogChannelID)
    await channel.send("Could not find new game message sending default new game message")
    await channel.send(e)

async def FuturePingPost(message):
  global FuturePing
  mess = message.content
  FuturePing = " " + mess[mess.index(" "):(len(mess)+1)].strip()
  await message.channel.send(FuturePing + " will be the next ping message to be sent")

async def NoPing(message,NoPing):
 try:
  await message.channel.send("Attempting to add this uhc to the non Ping list")
  mess = message.content.split(" ")[1]
  if "/" in mess:
    mess = mess[mess.rindex("/")+1:]  
    NoPing.append(mess)
    with open("UHC Bot/NoPingList.txt", "wb+") as myFile:
     pickle.dump(NoPing, myFile)
  else:
    await message.channel.send("Could not add to list invalid command format?")
 except:
    await message.channel.send("Could not add to Non Ping list")

async def NoPost(message,NoPost):
 try:
  await message.channel.send("Attempting to add this UHC game to the nonpost list")
  mess = message.content.split(" ")[1]
  if "/" in mess:
    mess = mess[mess.rindex("/")+1:]  
    NoPostList.append(mess)
    with open("UHC Bot/NoPostList.txt", "wb+") as myFile:
     pickle.dump(NoPostList, myFile)
  else:
    await message.channel.send("Could not add to list invalid command format?")
 except:
  await message.channel.send("Could not add to nopost list, if you are panicking use !auto off to turn off the automatic posting")

def CheckPost(MatchInfo):
 StaffList = [
    "C_moneySmith",
    "adorablur",
    "AlgoHost",
    "AtomicCrossbow",
    "CarbonateCO3",
    "CxlibriPlays",
    "DaniDeVit0",
    "Dashetoboba",
    "DIISU",
    "ElTioDodo",
    "Gronyak124",
    "JJQ4",
    "DaDoshua",
    "zombi3s_",
    "MSIPig",
    "NeededCheese",
    "rachammc",
    "Sicced",
    "TheMainMiek",
    "ImHab",
    "Andronifyy",
    "Sharkbob94349"
  ] 

 return ((MatchInfo["address"].lower() == "apollouhc.com") and (not (str(MatchInfo["id"]) in NoPostList))) and (MatchInfo["author"] in StaffList)


async def PendingtoAnnounce():
 ThirtyMinute = datetime.timedelta(hours = 0, minutes = 30)
 GamesList = await GetGamesUpcoming()
 for i in range(len(GamesList)):
   MatchTime = TimeTillMatch(GamesList[i])
   if MatchTime < ThirtyMinute:
    if CheckPost(GamesList[i]):
      await AnnounceGameAuto(GamesList[i],NoPostList,NoPingList)
 return

async def GetGamesUpcoming():
 link = "http://hosts.uhc.gg/api/matches/upcoming"
 r = requests.get(link)
 Matches = r.json()
 FilteredMatches = []
 for i in range(len(Matches)):
  if (not Matches[i]["removed"]):
    FilteredMatches.append(Matches[i])
 return FilteredMatches


@tasks.loop(seconds = 60) 
async def myLoop():
 if client.is_ready():
  try:
   await PendingtoAnnounce()
  except Exception as e:
   channel = client.get_channel(LogChannelID)
   await channel.send(e)


async def sendGameWinners(status):
 global LastGameID
 if not LastGameID == None:
  print(LastGameID)
  print(type(LastGameID))
  r = requests.get("https://hosts.uhc.gg/api/matches/" + str(LastGameID))
  MatchInfo = r.json()
  GameInfo = MakeShortPost(MatchInfo,True)
 try:
  channel = client.get_channel(LogChannelID)
  await channel.send(GameInfo + "\n\n" + status.text[:status.text.index("https:")]+"\n" + status.entities["media"][0]["media_url_https"]) 
 except Exception as e:
  try:
   channel = client.get_channel(LogChannelID)
   await channel.send(GameInfo + "\n\n" + status.text[:status.text.index("https:")]+"\n" + status.entities["media"][0]["media_url"]) 
  except:
   pass
  print(e)



async def HelpMessage(message):
 try:
  embed = discord.Embed(title="MatchPost Bot Commands",description = "All Commands for the MatchPost Bot Start with '!' here are a list of commands that can currently be used",color = discord.Color.dark_red())
  embed.add_field(name = "help",value = "Returns this help message",inline = True)
  embed.add_field(name = "status", value = "Shows current status of the apollo server including number of players online and MOTD data, useful for seeing game state or if whitelist is off",inline = True)
  embed.add_field(name = "scen [Scenario Name]",value = "returns a description of a scenario from the apollo scenario pastebin, unofficial scenarios not on the pastebin are not supported and some spell correction is applied to make the command easier to use", inline = True)
  embed.add_field(name = "trscen [Language] [Scenario Name]", value = "gives a computer translation of the given scenario name (translations may not be perfect",inline = True)
  embed.add_field(name = "nh [IGN]",value = "gives the recent name history of the given ign",inline = True)
  embed.add_field(name = "player [IGN]", value = "Gives a rendered image of the player's skin based off the ign", inline = True)
  embed.add_field(name = "hostinfo [Host Alias]", value = "Currently Disabled", inline = True) 
  embed.add_field(name = "staff", value = "Provides a list of aliases for all current and prior apollo staff, these aliases can be used in the hostinfo command instead of the uhc.gg account name", inline = True)
  embed.add_field(name = "matches",value = "Shows upcoming apollo matches on the uhc.gg calendar, make sure to pay attention to the date listed",inline = True)
  embed.set_footer(text = "Bot Developed by Algo")
  await message.reply(embed = embed,mention_author=False)
  
 except:
  await message.reply("Could not return Help message?",mention_author = False)
 
async def wlhelpmessage(message):
  AnnounceChannelString = "<#" + str(AnnouncementChannelID) + ">"
  rolesList = message.author.roles
  if len(rolesList) < 3:
    await message.author.send("The whitelist will open shortly before a game starts, only join when it says the wl is off and the host says so in general chat usually shortly before the game is scheduled to start on uhc.gg, nobody gets preference or pre-wl based on rank. if you have New Game role, you'll be pinged in" + AnnounceChannelString + " 30 minutes before a game opens, and again when it is about to begin",mention_author=False)
    await message.add_reaction("\N{INCOMING ENVELOPE}")




async def GetPlayerHistory(message):
 try:
  mess = message.content
  Player = mess[mess.index(" ")+1:]
  Player = Player.replace(" ","")
  uuid = MojangAPI.get_uuid(Player)
  NameHistory = MojangAPI.get_name_history(uuid)
  print (NameHistory)
  Names = "The Name History for this Player is the following (Last 10 Changes): \n"
  for i in reversed(range(min(len(NameHistory),10))):
    TimeStamp = math.ceil(NameHistory[i]["changed_to_at"] / 1000)
    if not TimeStamp == 0:
     Time = "[" + (dt.fromtimestamp(TimeStamp)).strftime("%m/%d/%Y") + "]"
    else:
     Time = "[Original Name]"

    Names = Names + "**" + NameHistory[i]["name"].replace("_","\_") + "**" + " " + Time + "\n"
  await message.reply(Names,mention_author=False)
 except Exception as e:
  print(e)
  await message.reply("Could not get Name History", mention_author = False)

async def GetPlayer(message):
 try:
  mess = message.content
  Player = mess[mess.index(" ")+1:]
  Player = Player.replace(" ","")
  im = await MinePI.render_3d_skin(Player,aa = True,ratio = 24) 
  im.save(Player +".png")
  await message.reply(file=discord.File(Player +".png"),mention_author = False)
  os.remove(Player+".png")
 except Exception as e:
  print(e)
  await message.reply("Could not get skin",mention_author = False)


######################################## Chest Simulator
def GetNumRolls(Roll):
 if type(Roll) is dict:
   if Roll["type"] == "minecraft:uniform":
     NumRolls = random.randint(Roll["min"],Roll["max"])
 if type(Roll) is int or type(Roll) is float:
   NumRolls = int(Roll)

 return NumRolls


def GetLootList(Entries):
 LootList = []

 for Entry in Entries:
  if "weight" in Entry.keys():
   LootList.extend([Entry] * Entry["weight"])
  else:
   LootList.append(Entry)

 return LootList



def GetLootFromPool(Pool):
  LootList = GetLootList(Pool["entries"])
  Rolls = GetNumRolls(Pool["rolls"])
  Loot = []
  for i in range(Rolls):
   Loot.append(random.choice(LootList))

  return Loot

def GetCount(LootItem,function):
  Count = function["count"]
  if type(Count) in [int,float]:
    Count = int(Count)
  if type(Count) is dict:
    if Count["type"] == "minecraft:uniform":
      Count = random.randint(Count["min"],Count["max"])
  
  return Count 



def ApplyFunctions(LootItem):
 Functions = LootItem["functions"]
 Value = None
 for func in Functions:
   if func["function"] == "minecraft:set_count":
    Value = GetCount(LootItem,func)

   
 return (LootItem, Value)


def AddItemToImage(ChestBackGround,Item,Slot):
 
 Item = Image.open("UHC Bot/ItemTextures/" + Item + ".png").convert("RGBA").resize((64,64))





 Ycord = (int(Slot / 9) * 70) + 60
 Xcord = ((Slot % 9) * 72) + 10

 ChestBackGround.paste(Item,(Xcord,Ycord),Item)
 return ChestBackGround

async def Loot(message):

 try:
  ChestVariety = message.content.split()[1].lower().replace(" ","")
 except:
  ChestVariety = None
 Chests = {
 "dungeon":"UHC Bot/JSON FILES MC/simple_dungeon.json",
 "treasure":"UHC Bot/JSON FILES MC/buried_treasure.json",
 "temple":"UHC Bot/JSON FILES MC/desert_pyramid.json",
 "bastion":"UHC Bot/JSON FILES MC/bastion_treasure.json",
 "city":"UHC Bot/JSON FILES MC/end_city_treasure.json",
 "bonus":"UHC Bot/JSON FILES MC/spawn_bonus_chest.json",
 "mineshaft":"UHC Bot/JSON FILES MC/abandoned_mineshaft.json",
 "portal":"UHC Bot/JSON FILES MC/ruined_portal.json",
 "mansion":"UHC Bot/JSON FILES MC/woodland_mansion.json"
 }
 if ChestVariety in list(Chests.keys()):
   ChestVariety = Chests[ChestVariety]
 else:
  ChestVariety = Chests["dungeon"]
 

 with open(ChestVariety) as json_file:
    data = json.load(json_file)


 LootTablePools = data["pools"]


 Loot = []
 for i in range(len(LootTablePools)):
  Loot = Loot + GetLootFromPool(LootTablePools[i])

 # Loot = List of loot before applying functions


 for i in range(len(Loot)):
  if not "functions" in Loot[i].keys():
   Loot[i] = (Loot[i],None)
  else:
   Loot[i] = ApplyFunctions(Loot[i])

 #Loot After Aplying Functions
 ChestInventory = []
 for Item in Loot:
  try:
   ChestInventory.append(Item[0]["name"].replace("minecraft:","").replace("book","enchanted_book"))
  except Exception as e:
   print(e)

 ChestInventory = ChestInventory[0:27]
 PadLength = 27 - len(ChestInventory)

 ChestInventory = ChestInventory + [None] * PadLength


 random.shuffle(ChestInventory)

 BackGround = Image.open("UHC Bot/chest_gui.png").convert("RGBA")
 Chest = BackGround.copy()


 for i in range(len(ChestInventory)):
  if not ChestInventory[i] == None:
   Chest = AddItemToImage(Chest,ChestInventory[i],i)
 
 ImageName = "UHC Bot/" + str(uuid.uuid4()) + ".png"
 Chest.save(ImageName)

 with open(ImageName,"rb") as f:
   picture = discord.File(f)
   await message.reply(file = picture,mention_author=False)
 os.remove(ImageName)
















async def ScenarioMessageTranslated(message):
  try:
   if len(message.content) > 6:
    mess = message.content.split(" ",2)
    print(mess)
    ScenarioName = mess[2].lower().replace(" ","").replace("?","").replace("_","").replace("-","")
    with open("UHC Bot/ScenarioInfo.txt", "rb") as myFile:
     ScenarioDictionary = pickle.load(myFile)
    ScenName = difflib.get_close_matches(ScenarioName,list(ScenarioDictionary.keys()),cutoff = 0.7)[0]
    ScenarioMessage = ScenarioDictionary[ScenName]
    print(ScenarioMessage)
    Language = languages[mess[1].lower().capitalize()]
    print(Language)
    ScenarioMessage = translate.translate(ScenarioMessage,"en-"+Language)
    print(ScenarioMessage)
    await message.reply(ScenarioMessage["text"][0],mention_author=False)
   else:
     await message.reply("Please add a scenario",mention_author=False)
  except Exception as e:
   await message.reply("Scenario Unavailable in that language, a list of scenarios on the server can be found at https://pastebin.com/PixjeKaS",mention_author=False)
   print(e)    




async def GetLanguages(message):
  await message.reply("The Supported languages are the following: " + (str(list(languages.keys()))).replace("[","").replace("]","").replace("'",""))



async def ScenarioScramble(message):
  with open("UHC Bot/ScenarioInfo.txt", "rb") as myFile:
     ScenarioDictionary = pickle.load(myFile)
  ScenarioList = list(ScenarioDictionary.values())
  Scenario = random.choice(ScenarioList)
  ScenarioName = Scenario[:Scenario.index(":")]
  print(ScenarioName)
  ScenarioListName = list(ScenarioName)
  random.shuffle(ScenarioListName)
  ShuffledName = ''.join(ScenarioListName)
  print(ShuffledName)
  
  await message.reply("Type the name of the following Scenario: " + ShuffledName,mention_author=False)
  start = time.time()
  
  def check(author):
    def inner_check(message):
        return message.author == author and message.content.upper() == ScenarioName.upper()
    return inner_check

  try:  
   msg = await client.wait_for("message", check=check(message.author), timeout=60.0)
  except Exception:
   await message.reply("You Ran Out of time!, Correct Answer was " + ScenarioName,mention_author=False)
  
  end = time.time()
  await msg.reply("This Is the correct Answer! You Answered in " + str(math.ceil((end-start)*10)/10) + " Seconds",mention_author=False)

async def Leaderboards(message):
 try:
  with open("UHC Bot/Scramble.txt", "rb+") as myFile:
   Scrambleinfo = pickle.load(myFile)
   Scrambleinfo.sort()
  with open("UHC Bot/RoleConversion.txt","rb+") as myFile:
   RoleNameToIDConversion = pickle.load(myFile)
  with open("UHC Bot/ScramDictionary.txt","rb+") as myFile:
   ScramDictionary = pickle.load(myFile)
 
  print(RoleNameToIDConversion)
  print(ScramDictionary)
  try:
   LeaderboardType = message.content.lower().split(" ")[1]
  except:
   LeaderboardType = "fastest"
  
  if LeaderboardType == "fastest":
   embed=discord.Embed(title="Leaderboard",description="This Leaderboard shows the fastest times", color=discord.Color.dark_blue())
 
   UserNames = ""
   Scenario = ""
   Times = ""
   for i in range(15):
    try:
     UserNames = UserNames + Scrambleinfo[i][3] + "\n"
     Scenario = Scenario + Scrambleinfo[i][2] + "\n"
     Times = Times + str(Scrambleinfo[i][0]) + "\n"
    except:
     pass
   embed.add_field(name="User", value=UserNames, inline=True)
   embed.add_field(name="Scenario", value=Scenario, inline=True)
   embed.add_field(name="Time", value=Times, inline=True)


   await message.reply(embed = embed,mention_author=False)
 except:
   await message.reply("Could not get Leaderboard",mention_author=False)


async def ScramStats(message):
 try:
  with open("UHC Bot/RoleConversion.txt","rb+") as myFile:
   RoleNameToIDConversion = pickle.load(myFile)
  with open("UHC Bot/ScramDictionary.txt","rb+") as myFile:
   ScramDictionary = pickle.load(myFile)
 
  MessTokens = message.content.lower().split(" ")
  
  if not (len(MessTokens) > 1):
   NameIndex = str(message.author).lower()
  else:
   NameIndex = MessTokens[1]

  IDIndex = RoleNameToIDConversion[NameIndex]
  info = ScramDictionary[IDIndex]
  embed=discord.Embed(title=NameIndex.upper() + " Scramble Stats", color=discord.Color.dark_blue())

  Time = round(info[1] / info[0],2)

  embed.add_field(name="Scrambles Solved", value=info[0], inline=True)
  embed.add_field(name="Average Time", value=Time, inline=True)
  await message.channel.send(embed = embed)
 except:
  await message.reply("Could not get Scramble Stats",mention_author = False)

async def ScenarioScrambleComp(message):
  Scrambleinfo = []
  try:
   with open("UHC Bot/Scramble.txt", "rb+") as myFile:
     Scrambleinfo = pickle.load(myFile)
  except Exception as e:
   print(e)
   

  with open("UHC Bot/ScenarioInfo.txt", "rb") as myFile:
     ScenarioDictionary = pickle.load(myFile)


  try:
   with open("UHC Bot/ScramDictionary.txt","rb+") as myFile:
     ScramDictionary = pickle.load(myFile)
  except:
     ScramDictionary = {}


  ScenarioList = list(ScenarioDictionary.values())
  Scenario = random.choice(ScenarioList)
  ScenarioName = Scenario[:Scenario.index(":")]
  print(ScenarioName)
  ScenarioListName = list(ScenarioName)
  random.shuffle(ScenarioListName)
  ShuffledName = ''.join(ScenarioListName)
  print(ShuffledName)
  await message.reply("Type the name of the following Scenario: " + ShuffledName,mention_author=False)
  start = time.time()
  
  def check(author):
    def inner_check(message):
        return (message.content.lower() == ScenarioName.lower()) and (message.author == author)
    return inner_check

  try:  
   msg = await client.wait_for("message", check=check(message.author), timeout=60.0)
   end = time.time() - client.latency
   timetook = (math.ceil((end-start)*100)/100)
   await msg.reply("This Is the correct Answer! You Answered in " + str(timetook) + " Seconds",mention_author=False)
  except Exception:
   timetook = 60
   await message.reply("You Ran Out of time!, Correct Answer was " + ScenarioName,mention_author=False)
  
  
  try:
   with open("UHC Bot/RoleConversion.txt","rb+") as myFile:
    RoleNameToIDConversion = pickle.load(myFile)
  except:
   RoleNameToIDConversion = {}

  RoleNameToIDConversion[str(message.author).lower()] = message.author.id
  Scrambleinfo.append((timetook,str(message.author.id),ScenarioName,str(message.author)))
  

  if message.author.id not in ScramDictionary:
    ScramDictionary[message.author.id] = (1,timetook)
  else:
    ScramDictionary[message.author.id] = (ScramDictionary[message.author.id][0] +1, ScramDictionary[message.author.id][1] + timetook)
  
  try:
   with open("UHC Bot/Scramble.txt", "wb+") as myFile:
    pickle.dump(Scrambleinfo, myFile)
  except Exception as e:
   print(e)


  try:
   with open("UHC Bot/ScramDictionary.txt", "wb+") as myFile:
    pickle.dump(ScramDictionary, myFile)
  except Exception as e:
   print(e)

  try:
   with open("UHC Bot/RoleConversion.txt", "wb+") as myFile:
    pickle.dump(RoleNameToIDConversion, myFile)
  except Exception as e:
   print(e)
   


async def ScenariosAdd(message):
 mess = message.content.split(" ",1)[1]
 print(mess)
 ScenarioName = mess.split(":",2)[0].strip()
 ScenarioDescription = mess.split(":",2)[1].strip()
 
 try:
  with open("UHC Bot/ExtraScenarioInfo.txt", "rb") as myFile:
   ExtraScenarios = pickle.load(myFile)
 except:
   ExtraScenarios = {}

 ExtraScenarios[ScenarioName] = ScenarioName + ": " + ScenarioDescription

 with open("UHC Bot/ExtraScenarioInfo.txt", "wb") as myFile:
  pickle.dump(ExtraScenarios, myFile)
 await ScenariosLoad(message)


async def ScenariosLoad(message):
 r = requests.get("https://pastebin.com/raw/PixjeKaS").text
 scens = r
 scens = scens.replace("\r","")
 scens = scens.split("\n")
 ScenList = []
 for i in range(len(scens)):
   if len(scens[i]) > 3:
     ScenList.append(scens[i])

 scens = ScenList
 
 scenName = []
 try:
  with open("UHC Bot/ExtraScenarioInfo.txt", "rb") as myFile:
   ScenarioDictionary = pickle.load(myFile)
 except:
  ScenarioDictionary = {}
 scens.pop(0) #removes the ApolloUHC Scenario List: element at the top
 for i in range(len(scens)):
  scenName = scens[i][:(scens[i].index(":"))].lower().replace(" ","").replace("?","").replace("_","").replace("-","")
  ScenarioDictionary[scenName] = scens[i]
 with open("UHC Bot/ScenarioInfo.txt", "wb") as myFile:
  pickle.dump(ScenarioDictionary, myFile)
 myFile.close()  
 await message.channel.send("Scenarios Sucessfully Loaded")

async def ScenarioMessage(message):
  try:
   if len(message.content) > 6:
    mess = message.content
    ScenarioName = mess[mess.index(" "):(len(mess)+1)].lower().replace(" ","").replace("?","").replace("_","").replace("-","")
    with open("UHC Bot/ScenarioInfo.txt", "rb") as myFile:
     ScenarioDictionary = pickle.load(myFile)
    ScenName = difflib.get_close_matches(ScenarioName,list(ScenarioDictionary.keys()),cutoff = 0.7)[0]
    await message.reply(ScenarioDictionary[ScenName],mention_author=False)
   else:
     await message.reply("Please add a scenario, Scen List: https://pastebin.com/PixjeKaS",mention_author=False)
  except Exception as e:
   await message.reply("Scenario Unavailable, a list of scenarios on the server can be found at https://pastebin.com/PixjeKaS",mention_author=False)
   print(e)


def FilterGames(GamesList):
  NewGamesList = []
  print(len(GamesList))
  for i in range(len(GamesList)):
    if (not GamesList[i]["removed"]) and (("apollouhc" in GamesList[i]["address"].lower()) or GamesList[i]["address"] == "apollouhc.net" or "Apollo" in GamesList[i]["tags"]):
      NewGamesList.append(GamesList[i])
  return NewGamesList
    
def TimeTillMatch(MatchInfo):
 r = requests.get("https://hosts.uhc.gg/api/sync").text
 CurrentTime = iso8601.parse_date(r[1:-1])  
 GameTime = iso8601.parse_date(MatchInfo["opens"])
 return GameTime - CurrentTime

def TimeTillMatchReadable(GameID):
 try: 
  r = requests.get("https://hosts.uhc.gg/api/sync").text
  print(r)
  CurrentTime = iso8601.parse_date(r[1:-1])  
  r = requests.get("https://hosts.uhc.gg/api/matches/" + str(GameID))
  MatchInfo = r.json()
  GameTime = iso8601.parse_date(MatchInfo["opens"])
  Time = GameTime - CurrentTime
  Time = Time - datetime.timedelta(microseconds=Time.microseconds)
  Time = humanfriendly.format_timespan(Time)
  if Time.startswith("-"):
   return "Game already Open"
  else:
   return Time
 except:
   return "Could not get time"

async def Matches(message):
 try:
  r = requests.get("https://hosts.uhc.gg/api/matches/upcoming")
  Matches = r.json()
  Matches = FilterGames(Matches)

  if len(Matches) > 0:
   Match = "Here are the Current Upcoming Matches currently on the uhc.gg calendar \n\n"
   for i in range(len(Matches)):
    Match = Match + MakeShortPost(Matches[i]) + "\n\n"
   await message.reply(Match,mention_author=False)
  else:
   await message.reply("There are currently no upcoming Apollo Matches posted",mention_author=False)
 except:
   await message.reply("Could not Retrieve Matches",mention_author=False)



async def GetAlias(message):
 print("hello")
 StaffAliasList = {
    "c_money":"C_moneySmith",
    "moog":"adorablur",
    "algo":"AlgoHost",
    "crossbow":"AtomicCrossbow",
    "carbo":"CarbonateCO3",
    "cxlibri":"CxlibriPlays",
    "dani":"DaniDeVit0",
    "dash":"Dashetoboba",
    "disu":"DIISU",
    "eltio":"ElTioDodo",
    "gronyak":"Gronyak124",
    "jackjack":"JJQ4",
    "josh":"DaDoshua",
    "loaf":"zombi3s_",
    "msi":"MSIPig",
    "needed":"NeededCheese",
    "racham":"rachammc",
    "sicced":"Sicced",
    "miek":"TheMainMiek",
    "hab":"ImHab",
    "sharkbob":"Sharkbob94349",
    "andro":"Andronifyy",
    "cheetah":"CheetaaahReddit",
    "andyboy":"Andyboyonalert",
    "sammy":"AyeeSammy14",
    "uglysheep":"_UglySheep_",
    "wack":"WackMaDino",
    "slushy":"Slushybunion",
    "tiny":"TinyxNinja",
    "mickae":"Mihkeeee",
    "plan":"p1an_",
    "samnumbers":"sam03062",
    "lordjack":"LordJxck",
    "slushy":"Slushybunion",
    "atomicbelch":"PingasPootis"
  }
 StaffString = "Current Staff: " + ", ".join(list(StaffAliasList.keys())[:22])
 print("hello")
 StaffString = StaffString + "\n" + "Former Staff: " + ", ".join(list(StaffAliasList.keys())[22:])
 await message.reply(StaffString,mention_author=False)

async def GetStatus(message):
 try:
  server = MinecraftServer.lookup("apollouhc.com")
  status = server.status()
  ServerInfo = status.raw
  Players = str(status.players.online) + "/" + str(status.players.max)
  motdList = ServerInfo["description"]["extra"]
  motd = ""
  for i in range(len(motdList)):
   motd = motd + motdList[i]["text"]

  embed=discord.Embed(title="Apollo Twitter", url="https://twitter.com/ApolloUHC_",color = discord.Color.dark_blue())
  embed.add_field(name="Players Online", value=Players, inline=True)
  embed.add_field(name="Status", value=motd, inline=True)
  await message.reply(embed = embed,mention_author=False)
 except:
  await message.reply("Could Not Retrieve Status: This May Mean That the Apollo Server is Resetting, **please do not attempt to join** until WL is **OFF**",mention_author=False)


async def SendMatchPostTweet(ID):
  RemovedScenarios = 0
  MatchPost = MakePost(ID,RemovedScenarios)

  while len(MatchPost) > 279:
    RemovedScenarios += 1
    MatchPost = MakePost(ID,RemovedScenarios)

  return api.update_status(status = MatchPost)

async def AnnounceMP(message):
 try:
  start = time.time()
  await message.channel.send(AttemptMessage)
  mess = message.content  
  Glink = (mess[mess.index(" "):(len(mess)+1)])
  ID = Glink[Glink.rindex("/")+1:] 
  channel = client.get_channel(AnnouncementChannelID)
  MatchPost = MakePost(ID)
  matchP = await channel.send(NewGameRole + MatchPost)
  await matchP.publish()
  try:
   tweet = await SendMatchPostTweet(ID)
   await message.channel.send(twitterLink+str(tweet.id))
  except:
   channel = client.get_channel(LogChannelID) 
   await channel.send("Could Not Send Tweet/TweetLink")
  end = time.time()
  await message.channel.send("MatchPost was **Announced** in " + channel.name + " [" + str(math.ceil((end-start)*10)/10) + "s]")
 except Exception as e:
   await message.channel.send(e)

def GetOpenTime():
  times = list(rrule(MINUTELY,interval=15,dtstart=datetime.date.today(),count=96))
  
  GameTime = times[bisect.bisect(times,datetime.datetime.now())]
  GameTime = GameTime + datetime.timedelta(minutes = 30)
  OpenTime = GameTime.strftime("%H:%M")
  return OpenTime


async def Template(message):
  IP = "apollouhc.com"
  Host = "Host: " + str(message.author)[:str(message.author).index("#")]

  try:
   msg = message.content.split(" ",1)[1]
  
   Scenarios = msg.split(",")
  
   TeamSize = "Team Size: " + Scenarios.pop(0).strip()
   TeamSize = TeamSize.replace("Ffa","FFA")
   TeamSize = TeamSize.replace("random","Random")
   TeamSize = TeamSize.replace("market","Market")
   TeamSize = TeamSize.replace("Rvb","RvB")
   TeamSize = TeamSize.replace("Tox","ToX")

   with open("ScenarioInfo.txt", "rb") as myFile:
    ScenarioDictionary = pickle.load(myFile)
    ScenarioList = list(ScenarioDictionary.values())

   Scenarionames = []
   for i in range(len(ScenarioList)):
    if ":" in ScenarioList[i]:
     Scenarionames.append(ScenarioList[i][:ScenarioList[i].index(":")])


   ScenariosIdentifier = ",".join(Scenarios[0:]).lower().replace(" ","").split(",")
   if "meta" in ScenariosIdentifier:
    
    Index = ScenariosIdentifier.index("meta")
    Scenarios.pop(Index)
    Scenarios = ["Cutclean","Hasty Boys","Timber"] + Scenarios
 


   for i in range(len(Scenarios)):
    try:
     Scenarios[i] = difflib.get_close_matches(Scenarios[i],Scenarionames,cutoff = 0.6)[0]
    except:
     Scenarios[i] = Scenarios[i].strip()
     

   Scenarios = ("Game Modes: " + str(Scenarios).replace("'","").replace("[","").replace("]","")).strip()

  except Exception as e:
   print(e)
   Scenarios = "Game Modes: "
   TeamSize = "Team Size: " 




  try:
   VersionName = MinecraftServer.lookup(IP).status().raw["version"]["name"]
 
   VersionName = VersionName.split(" ")[-1]
   VersionName = "Version: " + VersionName
  except:
   VersionName = "1.17.1"
  


  try:
   OpenTime = "Open Time: " + GetOpenTime()
  except:
   OpenTime = "Open Time:"

  ServerIP = "Server IP: " + IP


  GameMatchPost = "```" + "\n".join((NewGameRole,Host,TeamSize,VersionName,Scenarios,OpenTime,ServerIP)) + "```"
  await message.reply(GameMatchPost,mention_author=False)




async def CreateMP(message):
 await message.channel.send("Trying to Create MatchPost")
 try:
  mess = message.content  
  Glink = mess[mess.rindex("/")+1:]
  print(Glink)
  await message.channel.send("```" + NewGameRole + MakePost(Glink)  + "```")
 except Exception as e:
  print(e)
  await message.channel.send("uh oh something happed")


def MakeShortPost(MatchInfo,ShorterPost = False):
 try:
  if not MatchInfo["hostingName"] == None:
   Host = "Host: " + MatchInfo["hostingName"]
  else:
   Host = "Host: " + MatchInfo["author"]

  #Scenarios
  Scenarios = "Game Modes: " + str(MatchInfo["scenarios"]).replace("'","").replace("[","").replace("]","")

  #TeamSize 
  if MatchInfo["teams"] == "custom":
   Teams = "Team Size: " + MatchInfo["customStyle"].capitalize()
  else:
   Teams = "Team Size: " + (MatchInfo["teams"].capitalize() + " To" + str(MatchInfo["size"])).replace("To0","ToX").replace("ToNone","")
 
 
  Time = "Time Till Match: " + TimeTillMatchReadable(MatchInfo["id"])
  MatchTime = "Open Time: " + MatchInfo["opens"][11:16] + " UTC" + " [" + MatchInfo["opens"][:10] + "]"

  #info stuff
  Teams = Teams.replace("Ffa","FFA")
  Teams = Teams.replace("random","Random")
  Teams = Teams.replace("market","Market")
  Teams = Teams.replace("Rvb","RvB")
  Teams = Teams.replace("Tox","ToX")
  Scenarios = Scenarios.replace("Hastey","Hasty")

  GameString = "\n".join((Host,Teams,Scenarios,Time,MatchTime))
  if ShorterPost:
   GameString = "\n".join((Host,Teams,Scenarios))
  #GameString = "\n" + Host + "\n" + Teams + "\n" + Scenarios + "\n" + Time + ""
  return GameString
 except Exception as e:
   print(e)

def MakePost(GameID,RemovedScens = 0):
 
 link= "http://hosts.uhc.gg/api/matches/" + GameID
 r = requests.get(link)
 MatchInfo = r.json()
 MatchInfo["content"] = ""
 
 #Host Name
 if not MatchInfo["hostingName"] == None:
  Host = "Host: " + MatchInfo["hostingName"]
 else:
  Host = "Host: " + MatchInfo["author"]

 #Scenarios
 #https://stackoverflow.com/questions/15715912/remove-the-last-n-elements-of-a-list
 ScenariosList = MatchInfo["scenarios"][:-RemovedScens or None]

 if RemovedScens > 0:
   ScenariosList.append("...")

 Scenarios = "Game Modes: " + str(ScenariosList).replace("'","").replace("[","").replace("]","")

 #Version
 Version = "Version: " + MatchInfo["version"]
 
 #TeamSize 
 if MatchInfo["teams"] == "custom":
   Teams = "Team Size: " + MatchInfo["customStyle"].capitalize()
 else:
   Teams = "Team Size: " + (MatchInfo["teams"].capitalize() + " To" + str(MatchInfo["size"])).replace("To0","ToX").replace("ToNone","")
 Time = "Open Time: " + MatchInfo["opens"][11:16] + " UTC"

 Teams = Teams.replace("Ffa","FFA")
 Teams = Teams.replace("random","Random")
 Teams = Teams.replace("market","Market")
 Teams = Teams.replace("Rvb","RvB")
 Teams = Teams.replace("Tox","ToX")
 Scenarios = Scenarios.replace("Hastey","Hasty")
 #info stuff
 ServerIP = "Server IP: " + MatchInfo["address"]
 GameLink = "https://hosts.uhc.gg/m/" + str(MatchInfo["id"])
 
 GameString = "\n".join((Host,Teams,Version,Scenarios,Time,ServerIP,GameLink))

 
 return "\n" + GameString

async def PingPost(message):
  mess = message.content
  try:
   #Finds the index of the first space and set's pm to all the message after it
   PingM = (mess[mess.index(" "):(len(mess)+1)])
   #Sets the channel to the prespecified channel
   channel = client.get_channel(AnnouncementChannelID)
   messP = await channel.send(NewGameRole + PingM)
   await messP.publish()
  except:
   await message.channel.send("Invalid Ping Command")

@client.event
async def on_member_remove(member):
  MemberRoles = member.roles[1:]
  for i in range(len(MemberRoles)):
    MemberRoles[i] = MemberRoles[i].id
  try:
   with open("UHC Bot/RolesList.txt", "rb") as myFile:
    RoleDictionary = pickle.load(myFile)
  except:
    RoleDictionary = {}
  RoleDictionary[str(member.id)] = MemberRoles
  with open("UHC Bot/RolesList.txt", "wb") as myFile:
   pickle.dump(RoleDictionary, myFile)

@client.event
async def on_member_join(member):
  print(member.id)
  with open("UHC Bot/RolesList.txt", "rb") as myFile:
   RoleDict = pickle.load(myFile)
   

  if str(member.id) in RoleDict.keys():
   Roles = RoleDict[str(member.id)]
   for i in range(len(Roles)):
    try:
     guild = member.guild
     role = get(guild.roles, id=Roles[i])
     await member.add_roles(role)
    except Exception as e:
     print(e)


@client.event
async def on_ready():
  print("Logged in as {0.user}".format(client))
  channel = client.get_channel(LogChannelID)
  await channel.send("Bot Online")
  myLoop.start()
  channel = client.get_channel(LogChannelID)
  await channel.send("Turning on auto game announcement") 


async def crafts(message):
   e = discord.Embed()
   e.set_image(url="https://cdn.discordapp.com/attachments/400125580210601986/858771632481894440/customcraftswip.png")
   e.set_footer(text = "Image By EltioDodo")
   await message.reply(embed = e,mention_author = False)


async def GetAnimal(message):
 try:
  if message.author == client.user:
   return
  if message.content.lower().startswith("!dog"):
   r = requests.get("https://random.dog/woof.json?ref=apilist.fun").json()
   await message.reply(r["url"],mention_author=False)
  if message.content.lower().startswith("!cat"):
   r = requests.get("https://api.thecatapi.com/v1/images/search").json()
   await message.reply(r[0]["url"],mention_author=False)
 except:
  await message.reply("Could not get a picture of cute animal sorry")




async def Auto(message):
 Signal = message.content.lower().split(" ")[1]

 if Signal == "off":
   await message.reply("Turning auto announcement off")
   try:
     myLoop.stop()
   except:
     await message.reply("could not disable autoposting loop, it might already be disabled")

 if Signal == "on":
   await message.reply("Turning auto announcement on")
   try:
    myLoop.start()
   except:
    await message.reply("could not enable autposting loop, it might already be enabled")


def IsStaff(Author):
  rolesList = Author.roles
  for i in range(len(rolesList)):
    rolesList[i] = rolesList[i].id 

  if (TrialStaffRoleID in rolesList) or (StaffRoleID in rolesList):
   return True
  return False


@client.event
async def on_message(message):
 
  
  if message.author == client.user:
    return
 
  if " wl " in message.content.lower() or "whitelist" in message.content.lower():
    await wlhelpmessage(message)

  if not message.content.lower().startswith("!"):
    return


  #Animal command 
  if (message.channel.id == DonorChannelID) and (message.content.lower().startswith(["!dog","!cat"])):
   await GetAnimal(message)
   return

  #Allows Staff to use bot in any channel 
  ChannelList = [BotChannelID,LogChannelID]
  if not ((message.channel.id in ChannelList) or IsStaff(message.author)):
   return

  PlayerCommands = {
   "!scen":ScenarioMessage,
   "!status":GetStatus,
   "!player":GetPlayer,
   #"!hostinfo":GeneralInfo,
   "!help":HelpMessage,
   "!staff":GetAlias,
   "!matches":Matches,
   "!scramble":ScenarioScrambleComp,
   "!leaderboard":Leaderboards,
   "!scramstats":ScramStats,
   "!nh":GetPlayerHistory,
   "!crafts":crafts,
   "!trscen":ScenarioMessageTranslated,
   "!languages":GetLanguages,
   "!loot":Loot
  }
  
  StaffCommands = {
  "!mpost":AnnounceMP,
  "!mcreate":CreateMP,
  "!mping":PingPost,
  "!loadscens":ScenariosLoad,
  "!scadd":ScenariosAdd,
  "!nextping":FuturePingPost,
  "!noping":NoPing,
  "!nopost":NoPost,
  "!template":Template,
  "!auto":Auto
  }



  Command = message.content.split(" ",1)[0]
  if Command in PlayerCommands:
    await PlayerCommands[Command](message)
    return
  elif (Command in StaffCommands) and IsStaff(message.author):
    await StaffCommands[Command](message)
  




client.run(ClientToken)
