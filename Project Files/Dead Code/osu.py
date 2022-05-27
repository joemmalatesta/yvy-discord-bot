#First iteration of this. 
#pretty poor... sorry

import profile
import requests
from pprint import pprint
from statistics import mode

API_URL = 'https://osu.ppy.sh/api/v2'
TOKEN_URL = 'https://osu.ppy.sh/oauth/token'
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxMzgwMSIsImp0aSI6ImQ2MzBjZGVlODI5YjQ5NTBiN2Q1MmJkNDMwNThlMDc1MTJmMDc1NDc3ZWFhZjViYmE4NjU4NmFjMWRkYTAxZTg2OTFkNjViMzQ3YjJhNGQ5IiwiaWF0IjoxNjQ5MzgxNDYzLjIyNDA5MywibmJmIjoxNjQ5MzgxNDYzLjIyNDA5NSwiZXhwIjoxNjQ5NDY3ODQwLjE2MjI5Mywic3ViIjoiIiwic2NvcGVzIjpbInB1YmxpYyJdfQ.LKUq--ljN4yXYUSuzUaKz3fgp6iGlfcZxRNGSdVXxbqqW6FuqH6m-fs2eDDk8CstjVN2nK2c8NYrnbDsXdmRHPsGo_VG066KsD88T1e8Usr6cqOqqGlWETMoyXg1UMeZUTod9etEOizvcMtnFz7JOFk2SyWjxqn21KR-en_unALF0f65VFoZMtPQdvjZEIQRoBplgAM8q6XgU2wDM43oBWA6npgRIFc1v27ud37r9_CZ-6C9v9F0L_I6nvl5nz7_3RlDl8A85JKQL3-GoW37EGS4_RuhPDmxX8Dp3r9PySPiPbm1DBlNcbJ65Lvai_MILJ0_F2hYodW95h2FhUY20v8i6CZCQM2M8Izl59qFsgrtTgPVfCVHbkRMi_VvOlIJBc2NfysCj7Ps6pSPagg7gfoIH8kp4JIMxhIfcP9kRlkPL33vjZOy0hetdFsYY7rswhZEOcMt27Vkoei63nnc0JUr0cpittDX3nvES57RmViCBE6Xz3-V2BK5tY20mxtHdDNDGEqYFgBbW4LrcRM1p7cKwYp4OcGi8v2PF3vicYK7wUm3wHHjCLaIzQYnHBWAvyEYm-5cKb9_LqfQhrxgKfIVYRSkQ6LfJYyRw9q3uXtbeiDTouJxQOfocPay5engvsHfORZ2BedaLyBFcreeHSFkIcZmZuwvREBRXDb08Lg'

def fetch_user(ID):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    params = {
        'mode': 'osu',
        'limit': 100
    }
    userInfo = requests.get(f'{API_URL}/users/{ID}/', params=params, headers=headers)
    pprint(userInfo.json())




def userInfo(ID):
    response = fetch_user(ID)
    userInfo.username = response.json()["username"]
    userInfo.supporter = response.json()["support_level"]
    userInfo.rank = response.json()['statistics']['global_rank']
    userInfo.country_rank = response.json()["statistics"]["country_rank"]
    userInfo.country = response.json()['country']['name']
    userInfo.accuracy = response.json()['statistics']['hit_accuracy']
    userInfo.pp = response.json()['statistics']['pp']
    userInfo.playtime = response.json()['statistics']['play_time']
    userInfo.avatar = response.json()['avatar_url']
    userInfo.discord = response.json()['discord']


def topPlay(ID):
    response = fetch_user(ID, 'plays')
    topPlay.accuracy = response.json()[0]['accuracy']
    topPlay.title = response.json()[0]['beatmapset']['title']
    topPlay.playpp = response.json()[0]['pp']


def playInfo(ID, num):
    response = fetch_user(ID, 'plays')
    playInfo.accuracy = response.json()[num]['accuracy']
    playInfo.title = response.json()[num]['beatmapset']['title']
    playInfo.playpp = response.json()[num]['pp']
    playInfo.pic = response.json()[num]['beatmapset']['covers']['cover']


#Topplay
def get_topPlayAccuracy():
    return topPlay.accuracy
def get_topPlayTitle():
    x = topPlay.accuracy
    return "{:.2f}".format(x)
def get_topPlayPP():
    return topPlay.playpp

#play of choice
def get_playInfoAccuracy():
    x = playInfo.accuracy
    return "{:.2f}".format(x)
def get_playInfoPP():
    return playInfo.playpp
def get_playInfoTitle():
    return playInfo.title
def get_playInfoPic():
    return playInfo.pic()

def get_username():
    return userInfo.username
def get_supportlevel():
    return userInfo.supporter
def get_rank():
    return userInfo.rank
def get_countryRank():
    return userInfo.country_rank
def get_country():
    return userInfo.country
def get_accuracy():
    x = userInfo.accuracy
    return "{:.2f}".format(x)
def get_PPcount():
    return userInfo.pp
def get_playtime():
    return userInfo.playtime
def get_avatar():
    return userInfo.avatar
def get_discord():
    return userInfo.discord






#Make random osu facts
    #Number of spinners in top 100 plays
    #Average amount of circles in top plays

