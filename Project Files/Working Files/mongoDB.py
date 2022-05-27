import certifi
import pymongo
from pymongo import MongoClient
import certifi
import datetime
import os


cluster = pymongo.MongoClient(f"mongodb+srv://{os.environ.get('MONGODB_USERNAME')}:{os.environ.get('MONGODB_PASS')}@cluster0.v1ixy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["discord"]
collection = db["osu!"]
#Username used as discord name


#Create new entry. set discord ID to ID to pull info from, add ID, Discord username, osu! profile, join date and location, last updated, and amount of uses of bot.
def addEntry(discordID, username, osuProfile, server):
    time = currentTime()
    post = {"_id": discordID, "name":username, "profile":osuProfile, "joined from": server, "time registered" : time, "last updated": time, "uses": 1 }
    #try block fails if there is already a profile associated with the discord.
    try:
        collection.insert_one(post)
        #if no exception thrown, this is the users first mongo entry and will use the word 'set'
        return "set"
    except pymongo.errors.DuplicateKeyError:
        #if there is already a mongo entry with the discord ID, then update so as not to update time registered, and where registered from.
        updateProfile(discordID, osuProfile)
        return "updated"
        
        
#Find the osu! profile associated with the discord account (ID). Maybe also make a function that returns uses for a fun command.
def findProfile(discordID):
    try:
        #There shouldn't ever be a list as ID's can't overlap so always [0]
        prof = list(collection.find({"_id":discordID}))
        profile = ((prof)[0]["profile"])
        return profile
    except IndexError:
        #Return None to indicate there is no profile associated.
        return None


#Update profile information. Only allowed to update the profile name right now, and it updates last updated time.
def updateProfile(discordID, osuProfile):
    time = currentTime()
    collection.update_one({"_id": discordID}, {"$set":{"profile": osuProfile, "last updated": time} })

#used for getting current time just in general.
def currentTime():
    now = datetime.datetime.now()
    current = (now.strftime("%y-%m-%d %H:%M:%S"))
    return str(current)

#Add one to their use stat everytime they call the bot.
def incrementUse(discordID):
    collection.update_one({"_id": discordID}, {"$inc" : {"uses" : 1}})

