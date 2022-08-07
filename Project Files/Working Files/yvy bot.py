##THIS IS A Discord Bot.py rewrite. I will not include broken commands "Red Green Blue"
#Rewrite the *help command to put commands in either osu! or general catergory
#This, as much as possible will only be related to Discord API. 
#I will try not to add a ton of features beyond what I already have for the sake of time
#Hope to add a few useful general features, as well as a compare command for osu!.
#Would be cool to track for new top plays but logistically I don't know how that works really.
#Maybe come back and do that after.

#Im going to try and heavily comment so this code doesn't become a forgein language 
#Also try to stay consistant with my naming scheme. camelCase.
from ast import alias
from logging.config import valid_ident
from multiprocessing.sharedctypes import Value
from pydoc import describe
import discord
import random
from discord.ext import commands
import osurefactor
from discord import Embed
import time
import requests
import mongoDB
import time
import json
import certifi
import datetime
import os
from discord.ext.commands import CommandNotFound
import asyncio


client = commands.Bot(command_prefix="*", case_insensitive=True)
client.remove_command('help')


osurefactor.refreshToken() #Initialize the token
 

async def tokenTimer(): #Used to refresh the token before it expries. It expires in a day
    while True:
        await asyncio.sleep(80000)
        osurefactor.refreshToken()
        print("Token Refreshed")


@client.event
#Print when bot is up and ready for use
async def on_ready():
    print("Logged in as {0.user}".format(client))
    await tokenTimer()

#Creates a log of deleted messages. Yes I know it exists within discord already
@client.event
async def on_message_delete(message):
    print(f'{message.author} just deleted a message that read "{message.content}" in Server: {message.guild.name} || Channel: {message.channel.name}')


#Catch errors with typing commands. direct them to help command
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        #Should just put pass here so it's not annoying
        #pass
        await ctx.send("Invalid Command... use ***help** for a list of commands and their correct use")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("Missing a required field. refer ***help** for correct use case")
    else:
        raise error



#########          HELP         #########    
#TODO redo this with working and useful commands and seperate into two channel. Then be done with this project because I gotta move on.
@client.command(aliases=["commands", "h"])
async def help(ctx):
    #Increment bot use number
    mongoDB.incrementUse(ctx.author.id)

    embed = discord.Embed(color=ctx.author.color)
    embed.set_author(name= "*  yvy Commands  *", url  = 'https://github.com/McChikin/osu--simplified', icon_url=client.user.avatar_url)
    embed.add_field(name="General Commands", value= "send bugs or errors to Bin Reaper#2398", inline=False)
    embed.add_field(name="*Roll", value="Roll a number 1-100", inline= True)
    embed.add_field(name="*ping", value="Show Bot Latency ", inline = True)
    embed.add_field(name="*Clear __Amount__", value="Clear messages", inline=True)
    embed.add_field(name="*whois __Mention User__", value="Gives information on a user", inline=True)
    embed.add_field(name="*WordCount __Message__", value="Gives wordcount of text", inline=True)
    embed.add_field(name= "osu! commands", value="all commands for circle clickers", inline = False)
    embed.add_field(name= "*setprofile", value="connects your osu! profile with your discord")
    embed.add_field(name= "*osu", value= "Shows osu! profile stats. use *osu __osu! username__ to view their profile")
    embed.add_field(name="*recent", value= "Shows most recent play. use *recent __osu! username__ to view their recent play")
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")

    await ctx.send(content=None, embed=embed)


#########     GENERAL COMMANDS      #########  
#many are simple dumb commands I first made to help me learn. 



@client.command(aliases=["whois", "info"])
@commands.has_permissions(send_messages=True)
async def user(ctx, member : discord.Member):
    #Param member is the person tagged by the author.
    #elapsed time and increment use will be on most commands for backend testing and data
    start = time.time()
    mongoDB.incrementUse(ctx.author.id)
    embed2 = discord.Embed(title = member.name, description = member.mention , color = discord.Color.blurple())
    embed2.add_field(name = "ID", value = member.id , inline = False)
    embed2.add_field(name="Current Status", value=member.status, inline=False)
    embed2.set_thumbnail(url = member.avatar_url)
    embed2.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(content=None, embed=embed2)
    end = time.time()
    elapsed = end - start
    print(f'{ctx.author} used whois command for {member} in {elapsed}')


#wordcount command returns wordcount not inluding context.
# * param takes in all in between text. It is like *args
@client.command(aliases=["wc"])
async def wordCount(ctx, *, text):
    mongoDB.incrementUse(ctx.author.id)
    await ctx.message.delete()
    await ctx.send(f"{len(text.split())} Words")

#text moderation
#only usable by those with admin permissions.
#amount includes this message so add amount + 1 
@client.command(aliases=["purge"])
@commands.has_permissions(administrator=True)
async def clear(ctx, amount):
    mongoDB.incrementUse(ctx.author.id)
    await ctx.channel.purge(limit=(int(amount) + 1))
    print(f'{ctx.author} deleted {amount} of messages from {ctx.channel.name}')


#Roll command just for fun!
@client.command()
async def roll(ctx):
    mongoDB.incrementUse(ctx.author.id)
    responses = list(range(101))
    await ctx.send(f"{ctx.author.mention} Rolled {random.choice(responses)} points!")


#Sends the clients latency to the user.
@client.command(aliases=["latency", "lag"])
async def ping(ctx):
    mongoDB.incrementUse(ctx.author.id)
    await ctx.send(f"Bot Latency: {round(client.latency * 1000)}ms")





#########     OSU COMMANDS      #########      
#more solphisticated stuff here.     


#Set/Update osu! profile associated with discord account. 
#take params and add or update an account in MongoDB
@client.command(aliases=["setprofile", "osusetprofile", 'osuset', "setosu"])
async def osuAccountSetup(ctx, osuname):
    mongoDB.incrementUse(ctx.author.id)
    start = time.time()
    profile = osuname
    guild = (ctx.channel.name, ctx.guild.name, ctx.guild.id)
    addType = mongoDB.addEntry(ctx.author.id, str(ctx.author), profile, guild)
    nickname = ctx.author.nick
    if nickname == None:
        nickname = ctx.author.name
    await ctx.send(f"{nickname}, Your osu! profile has been succesfully {addType} to {profile} ```If you wish to change your profile, simply use this command again!```")
    end = time.time()
    elapsed = end-start
    print(f"{ctx.author} set their profile to {osuname}... This took {elapsed} seconds")


@client.command(aliases=["osu", "osuprofile", "osu!", "whoisosu"])
#MAKE THE SECOND ARGUMENT OPTIONAL LOOK INTO USING ARGS
async def profileOverview(ctx, osuname=None):
    start = time.time()
    mongoDB.incrementUse(ctx.author.id)
    #Check first if there was an argument given, if not check if there is a profile associated. If not return error message.
    if osuname == None:
        osuname = mongoDB.findProfile(ctx.author.id)
        if osuname == None:
            await ctx.send("There is not an osu! profile associated with this account")
            await ctx.send(f'Use command "*setprofile __osu! username__ to link your account')
            return
    player = osurefactor.fetchUser(osuname)
    username = player.username
    #Support level is 0 if player is not an osu! supporter 
    if player.supportlevel == 0:
        pass
    else:
        emoji = " ♥️"
        username = username + emoji #Simpler way to do this, but add heart if player is an osu! supporter.

    #Some calculation and formatting stuff So it cleans up the embed.
    playtimeDays = int(player.playtime/24/60/60)
    playtimeHours = int((player.playtime/3600)%24)
    playerAcc = '{:.2f}'.format(player.accuracy)
    playacc = '{:.2f}'.format(player.play.accuracy * 100 )


    #Embed the stuff. Not all is needed right now but whatever
    embed = discord.Embed(color=discord.Color.random())
    #link github in here. I like that little bit. Just gotta comit the final thing.
    embed.set_author(name = username, url = f"https://osu.ppy.sh/users/{osuname}", icon_url=player.userPic)
    embed.add_field(name=f'Rank: #{player.rank}', value=f"PP: {int(player.totalPP)}", inline= True)
    embed.add_field(name=f'Country Rank: #{player.countryRank}', value=f"Country: {player.country}", inline=True)
    embed.add_field(name=f'Acc: {playerAcc}%', value=f"Playtime: {playtimeDays} Days {playtimeHours} Hours", inline=False)
    embed.add_field(name=f'Top play: {player.play.title}', value=f'[Map Link]({player.play.url})', inline=False)
    embed.add_field(name=f'PP: {int(player.play.pp)}', value=f'Accuracy: {playacc}%  ⮞ [{player.play.threeHundredCount}/{player.play.hundredCount}/{player.play.fiftyCount}]  {player.play.missCount}X miss ', inline=True)
    embed.set_image(url=player.play.beatmapCover)
    embed.set_thumbnail(url=player.userPic)
    embed.set_footer(icon_url=ctx.author.avatar_url ,text=f"Requested by {ctx.author.name}")
    await ctx.send(content=None, embed=embed)
    end = time.time()
    elapsed = end - start
    print(f"{ctx.author} used the osu! command for player \"{osuname}\" in {elapsed} seconds")




#TODO make this more appealing to the eyes.
@client.command(aliases=['r', 'recent', 'rs', 'recentscore'])
async def recentPlay(ctx, osuname=None):
    start = time.time()
    mongoDB.incrementUse(ctx.author.id)
    #if osuname argument blank, find profile in database, if still blank throw an error and direct to help
    if osuname == None:
        osuname = mongoDB.findProfile(ctx.author.id)
        if osuname == None:
            await ctx.send(f'No account associated with {ctx.author}... Connect you osu! account to your discord using "*setprofile (your osu! username)"')
            return
    #Try to get recent play. If it throws out of bounds error, it means the player has no recent plays (No plays in last 24hr)
    try:
        player = osurefactor.fetchUser(osuname, 'recent')
    except IndexError:
        await ctx.send(f'No recent play found for {osuname}')
        return
    #Format accuracy    
    playacc =  '{:.2f}'.format(player.play.accuracy * 100 )

    #Make mods look pretty and make No Mod if mods is []
    mods = player.play.mods
    #if not mods: <------ ALSO WORKS
    if mods == []:
        mods = str('No Mod')
    else:
        mods = str(player.play.mods)
        replace = ("[,'] ")
        for characters in replace:
            mods = mods.replace(characters, '')
    #PP same issue. 
    pp = player.play.pp
    if pp == None:
        pp = 0

    #Kind of tedious making the embed for this. Tried styling this the way another bot did theirs but I'm missing some information and don't know where to get it.
    embed = discord.Embed(color = discord.Colour.random())
    embed.set_thumbnail(url=player.play.beatmapImage)
    embed.set_author(name =f'{player.play.title} [{player.play.mapDifficulty}] +{mods} [{player.play.starRating}★]', url = player.play.url, icon_url=player.userPic)
    embed.add_field(name=f"⮞ {player.play.letterRank}  ⮞  **{int(pp)}PP** ▸  {playacc}%", value= f"⮞ {player.play.score} ⮞ x{player.play.maxCombo}/{player.play.comboPossible} ⮞ [{player.play.threeHundredCount}/{player.play.hundredCount}/{player.play.fiftyCount}] ⮞ {player.play.missCount}❌", inline=False)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Recent play from {osuname}")
    await ctx.send(embed= embed)
    end = time.time()
    elapsed = end - start
    print(f"Recentplay used by {ctx.author} in {elapsed}")


#.env maybe? This finishes my bot and it runs that. Maybe on another refactor I make different cogs. Don't have time now to look into it.
client.run(os.environ.get("DISCORD_TOKEN"))
