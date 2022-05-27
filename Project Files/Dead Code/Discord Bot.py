from ast import alias
from pydoc import describe
import discord
import random
from discord.ext import commands
from discord import Embed
import time
import requests
import mongoDB
import time
import json
import certifi
import pymongo
from pymongo import MongoClient
import datetime
import os

client = commands.Bot(command_prefix="*", case_insensitive=True)
client.remove_command('help')


#discord.ext.commands.client.case_insensitive



@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

client.case_insensitive = True

#osu! portion... This is eseentially to create a whois fucntion but for their osu! profile.


#MONGODB DATABASE
cluster = pymongo.MongoClient(f"mongodb+srv://{os.environ.get('MONGODB_USERNAME')}:{os.environ.get('MONGODB_PASS')}@cluster0.v1ixy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["discord"]
collection = db["osu!"]



@client.command()
async def test(ctx, osuname):
    mongoDB.addEntry(ctx.author.id, str(ctx.author), osuname)
    await ctx.send("Done")
    

#Attatch an osu! account to a discord profile in order to 
@client.command(aliases=["setprofile", "osusetprofile", 'osuset', "setosu"])
async def osu_account_setup(ctx, osuname):
    start = time.time()
    profile = osuname
    mongoDB.addEntry(ctx.author.id, str(ctx.author), profile)
    nickname = ctx.author.nick
    if nickname == None:
        nickname = ctx.author.name
    await ctx.send(f"{nickname}, Your osu! profile has been set to {profile}... If you wish to change, Coming soon o.o")
    end = time.time()
    elapsed = end-start
    print(f"{ctx.author} set their profile to {osuname}... This took {elapsed} seconds")

@client.command()
async def name(ctx):
    await ctx.send(ctx.author.id)


@client.command(aliases=["profile", "myprofile", "findprofile"])
async def getProfile(ctx):
    try:
        prof = list(collection.find({"_id":ctx.author.id}))
        profile = ((prof)[0]["profile"])
    except IndexError:
        await ctx.send("No account with this ma")
    await ctx.send(f'your profile is {profile}')
    return profile
#REFACTOR THIS PART SO THAT I CAN PULL WHATEVE THE RUCK I WANT MAKE A CLAS FOR DATABASE
def get_Profile(name):
    prof = list(collection.find({"_id":name}))
    profile = ((prof)[0]["profile"])
    return profile


@client.command(aliases=["osu", "osuprofile", "osu!", "whoisosu"])
#MAKE THE SECOND ARGUMENT OPTIONAL LOOK INTO USING ARGS
async def osu_profile(ctx, osuname=None):
    start = time.time()
    name = ctx.author.id
    if osuname == None:
        osuname = get_Profile(name)
        if osuname == None:
            await ctx.send("There is not an osu! profile associated with this account")
            await ctx.send(f'Use command "*setprofile __osu! username__ to link your account')
            return
    player = osurefactor.fetch_user(osuname)
    username = player.username
    #Support level is 0 if player is not an osu! supporter 
    if player.supportlevel == 0:
        pass
    else:
        emoji = " :heart:"
        username = username + emoji

    #Some calculation and formatting stuff So it cleans up the embed.
    playtimeDays = int(player.playtime/24/60/60)
    playtimeHours = int((player.playtime/3600)%24)
    playerAcc = '{:.2f}'.format(player.accuracy)
    playacc = '{:.2f}'.format(player.play.accuracy * 100 )


    #Embed the stuff. Not all is needed right now but whatever
    embed = discord.Embed(color=discord.Color.random())
    embed.set_author(name = username, url = f"https://osu.ppy.sh/users/{osuname}", icon_url=player.userPic)
    #embed = discord.Embed(title=username, description=f"https://osu.ppy.sh/users/{osuname}", color=discord.Color.random())
    embed.add_field(name=f'Rank: #{player.rank}', value=f"PP: {int(player.totalPP)}", inline= True)
    embed.add_field(name=f'Country Rank: #{player.countryRank}', value=f"Country: {player.country}", inline=True)
    embed.add_field(name=f'Acc: {playerAcc}%', value=f"Playtime: {playtimeDays} Days {playtimeHours} Hours", inline=False)
    embed.add_field(name=f'Top play: {player.play.title}', value=f'[Map Link]({player.play.url})', inline=False)
    embed.add_field(name=f'PP: {int(player.play.pp)}', value=f'Accuracy: {playacc}%', inline=True)
    embed.set_image(url=player.play.beatmapCover)
    embed.set_thumbnail(url=player.userPic)
    embed.set_footer(icon_url=ctx.author.avatar_url ,text=f"Requested by {ctx.author.name}")
    await ctx.send(content=None, embed=embed)
    end = time.time()
    elapsed = end - start
    print(f"{ctx.author} used the osu! command for player \"{osuname}\" in {elapsed} seconds")



@client.command(aliases=['r', 'recent', 'rs', 'recentscore'])
async def recentplay(ctx, osuname=None):
    osuname = get_Profile(ctx.author.id)
    try:
        player = osurefactor.fetch_user(osuname, 'recent')
    except IndexError:
        await ctx.send(f'No recent play found for {osuname}')
        return
    start = time.time()
    if osuname == None:
        ctx.send(f'No account associated with {ctx.author}... Connect you osu! account to your discord using "*setprofile (your osu! username)"')
    playacc =  '{:.2f}'.format(player.play.accuracy * 100 )
    username = player.username
    if player.supportlevel == 0:
        pass
    else:
        emoji = " :heart:"
        username = username + emoji
    mods = str(player.play.mods)
    if not mods:
    #if mods == []:  <----- ALSO WORKS
        mods = 'No Mod'
    else:
        replace = ("[,'] ")
        for characters in replace:
            mods = mods.replace(characters, '')
    title = (f'{player.play.title} [{player.play.mapDifficulty}] +{mods} [{player.play.starRating}★]')
    pp = player.play.pp
    if pp == None:
        pp = 0

    embed = discord.Embed(color = discord.Colour.random())
    embed.set_thumbnail(url=player.play.beatmapImage)
    title = (f'{player.play.title} [{player.play.mapDifficulty}] +{mods} [{player.play.starRating}★]')
    embed.set_author(name = title, url = player.play.url, icon_url=player.userPic)
    embed.add_field(name=f"➟ {player.play.letterRank} ➟ {int(pp)} PP ➟ {playacc}%" , value=f"➟ {player.play.maxCombo}/{player.play.comboPossible} ➟ {player.play.missCount}✗ Miss")
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Recent play from {osuname}")
    await ctx.send(content= None, embed= embed)
    end = time.time()
    elapsed = end - start
    print(f"Recentplay used by {ctx.author} in {elapsed}")
    
    








































#Ping

@client.command(aliases=["latency", "lag"])
async def ping(ctx):
    await ctx.send(f"Bot Latency: {round(client.latency * 1000)}ms")

#roll

@client.command
async def roll(ctx):
    responses = list(range(101))
    await ctx.send(f"{ctx.author.mention} Rolled {random.choice(responses)} points!")

#nickname (in progress)

@client.command(aliases=["nickname"])
@commands.has_permissions(change_nickname=True)
async def nick(ctx, *, name):
    await ctx.author.update(nick=name)


#help command embed

@client.command(aliases=["commands", "h"])
async def help(ctx):
    embed = discord.Embed(title="*  __yvy Commands__ *", description="All commands for yvy", color= discord.Color.blue())
    embed.add_field(name="__*Roll__", value="Roll a number 1-100", inline= False)
    embed.add_field(name="__*ping__", value="Show Bot Latency ", inline = False)
    embed.add_field(name="__*Nick (Nickname)__", value="Chose your nickname", inline= False)
    embed.add_field(name="__*Clear (Amount)__", value="Clear messages (Only Available to Administrator", inline=False)
    embed.add_field(name="__*whois (Mention User)__", value="Gives information on a user", inline=False)
    embed.add_field(name="__*Green/Yellow/Blue (Message)__", value="Changes color of subsequent text", inline=False)
    embed.add_field(name="__*WordCount (Message)__", value="Gives wordcount of subsequent text", inline=False)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")

    await ctx.send(content=None, embed=embed)

#user info

@client.command(aliases=["whois", "info"])
@commands.has_permissions(send_messages=True)
async def user(ctx, member : discord.Member):
    embed2 = discord.Embed(title = member.name, description = member.mention , color = discord.Color.blurple())
    embed2.add_field(name = "ID", value = member.id , inline = False)
    embed2.add_field(name="Current Status", value=member.status, inline=False)
    embed2.set_thumbnail(url = member.avatar_url)
    embed2.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(content=None, embed=embed2)

#wordcount

@client.command(aliases=["wc"])
async def wordcount(ctx, *, text):
    await ctx.message.delete()
    await ctx.send(len(text.split()))

#text moderation

@client.command(aliases=["purge"])
@commands.has_permissions(administrator=True)
async def clear(ctx, amount):
    await ctx.channel.purge(limit=(int(amount)))

#color changes

@client.command(aliases=["g"])
async def green(ctx, *, text: str):
    await ctx.message.delete()
    await ctx.send(f"{ctx.author.nick}:```CSS\n{text}\n```")

@client.command(aliases=["b"])
async def blue(ctx, *, text: str):
    await ctx.message.delete()
    await ctx.send(f"{ctx.author.nick}:```ELM\n{text}\n```")

@client.command(aliases=["y"])
async def yellow(ctx, *, text: str):
    await ctx.message.delete()
    await ctx.send(f"{ctx.author.nick}:```HTTP\n{text}\n```")

#assign your own roles
























































#token
client.run(os.environ.get("DISCORD_TOKEN"))