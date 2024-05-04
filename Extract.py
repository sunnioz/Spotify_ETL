import pandas as pd 
import requests
from datetime import datetime
import datetime


USER_ID = "kx0m2mnq8thrarcqyhp8zj5zs" 
TOKEN = "BQDgAhC__j8ejMefNjZNcn4UrBZpu8IMeZEmVNAWBLPOZmT8H9d2TSlimP3BgJhlym_hhxztiSKGZ5wzKm3Ofr8FUGfK2vpe3cGJAHA6-xdMdfqetjZhZLV-0A_GmFavegHnKiaSi6K-sA7U0C8TfRJPrRdtJm83g3Uih0gtHtUJHateoKoqsgLSNqGo1i7ewwKbNN_SpdOY8AT9zG3B4tDX6yrmvv6LYRIptqufZw"
# Creating an function to be used in other python files
def return_dataframe(): 
    input_variables = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }
     
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=30)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # Download all songs you've listened to "after yesterday", which means in the last 24 hours      
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(time=yesterday_unix_timestamp), headers = input_variables)

    data = r.json()
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    # Extracting only the relevant bits of data from the json object      
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])
        
    # Prepare a dictionary in order to turn it into a pandas dataframe below       
    song_dict = {
        "song_name" : song_names,
        "artist_name": artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps
    }
    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp"])
    return song_df