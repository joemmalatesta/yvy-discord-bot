from dataclasses import dataclass
import profile
from textwrap import indent
from tokenize import TokenInfo
import requests
from pprint import pprint
from statistics import mode
import os
import time
import mongoDB
#Initialize some things 

API_URL = 'https://osu.ppy.sh/api/v2'
TOKEN_URL = 'https://osu.ppy.sh/oauth/token'


@dataclass
class Token:
    token : str
    expiryTime : int
    refreshToken : str
def getToken():
    data = {
        'client_id' : 13801,
        'client_secret' : os.environ.get('OSU_API_SECRET_KEY'), #using local env for now. Maybe .env file coming soon 
        'grant_type' : 'client_credentials',
        'scope' : 'public'
    }
    response = requests.post(TOKEN_URL, data=data)
    return Token(
        expiryTime= response.json().get('expires_in'),
        token = response.json().get('access_token'),
        refreshToken = response.json().get("refresh_token")
    )

token : str

def refreshToken(): #Little workaround I came up with to refresh the token before it expires.
    global token
    tokenInfo = getToken()
    token = tokenInfo.token
    print(tokenInfo.expiryTime)


@dataclass
class BeatMap: #double as class for plays
    title : str
    pp : int #play specific
    accuracy : float #play specific
    beatmapImage : str #Square one for thumbnail 
    beatmapCover : str #This is the long one I use for *osu command
    url: str
    mods: str #Play specific
    letterRank: str #play specific
    rankedStatus: int
    mapDifficulty : str #play specific - the map diff
    comboPossible : int #Total possible combo
    maxCombo : int #play specific -- max combo in the play
    starRating : float 
    missCount : int
    hundredCount : int
    fiftyCount : int
    threeHundredCount : int
    score : int





def fetchPlay(profileID, scoreType='best'): #Autos to best. Change to 'recent' if used for that command.
    headers = { 
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    params = {
        'mode': 'osu',
        'limit' : 1, #output a single map
        'include_fails' : 1 #Yes include them = 1
    }
    #ID is required for obtaining play Data, not just profile name.
    unreadablePlayData = requests.get(f'{API_URL}/users/{profileID}/scores/{scoreType}', params=params, headers=headers)
    playData = unreadablePlayData.json() #For converting into usable data in json format.
    try:
        beatmapID = playData[0]['beatmap']['id'] #First use of the json and first thing to throw an error if the token is invalid
    except KeyError: #Added support just in case the token does not properly refresh pre empitvely
        refreshToken()
    #Make a second call for more information on the map. Needed for getting the max combo. Maybe some more stuff in the future.
    unreadableMapData = requests.get(f'{API_URL}/beatmaps/{beatmapID}', params=params, headers=headers)
    mapData = unreadableMapData.json()
    return BeatMap( #Thanks Dale! This is a nice way of doing this
        comboPossible = mapData['max_combo'], #total possible combo
        accuracy = playData[0]['accuracy'],
        maxCombo = playData[0]['max_combo'], #Max from the play
        title = playData[0]['beatmapset']['title'],
        mods = playData[0]['mods'],
        pp = playData[0]['pp'],
        letterRank = playData[0]['rank'],
        url = playData[0]['beatmap']['url'],
        rankedStatus = playData[0]['beatmap']['ranked'], #returns 1 for yes
        mapDifficulty  = playData[0]['beatmap']['version'],
        beatmapImage = playData[0]['beatmapset']['covers']['list'],
        beatmapCover = playData[0]['beatmapset']['covers']['cover'], #url
        starRating = playData[0]['beatmap']['difficulty_rating'],
        missCount = playData[0]['statistics']['count_miss'],
        hundredCount = playData[0]['statistics']['count_100'],
        fiftyCount = playData[0]['statistics']['count_50'],
        threeHundredCount = playData[0]['statistics']['count_300'],
        score = playData[0]['score']
    )





@dataclass #not certain what this does but...
#rewriting my egregious thing in a class form. Will maintain methods as fetch_user
class User:
    username: str
    rank: int
    countryRank : int
    accuracy : float
    supportlevel : int #May end up being bool
    country : str
    totalPP : int
    playtime : int
    userPic : str
    userDiscord : str
    play : BeatMap #cool class structure. 



def fetchUser(profileName, scoreType='best'):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    params = {
        'mode': 'osu',
        'limit' : 1 #only one map is returned. Change up to 100 if you please.
    }
    unreadableData = requests.get(f'{API_URL}/users/{profileName}/', params=params, headers=headers)
    userData = (unreadableData.json())
    profileID = userData['id'] #Needed for getting play data, as username doesn't suffice for that
    return User(
        username = userData['username'],
        rank = userData['statistics']['global_rank'],
        countryRank = userData["statistics"]["country_rank"],
        accuracy= userData['statistics']['hit_accuracy'],
        totalPP= userData['statistics']['pp'],
        playtime = userData['statistics']['play_time'],
        userPic = userData['avatar_url'],
        userDiscord= userData['discord'],
        country = userData['country']['name'],
        supportlevel= userData["support_level"], #Returns 0 if not a supporter. Returns 1 if they are I think but had some issues with that.
        play = fetchPlay(profileID, scoreType)) 
