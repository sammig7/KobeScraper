'''
Kobe Bryant Signature Move Dataset
compile list of Kobe Bryant signature moves
find videos for each signature move
'''
from datetime import datetime
import csv
from operator import index
import pandas as pd
import os
from dotenv import load_dotenv
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from pprint import pprint



load_dotenv()
API_KEY = os.getenv('API_KEY')

class VideoData:
  def __init__(self, video_id, upload_date, video_url):
    self.video_id = video_id
    self.upload_date = upload_date
    self.video_url = video_url # https://www.youtube.com/watch?v={videoID}
    # self.signature_move = signature_move # to be labelled
    # self.timestamps = timestamps # start and end time, to be labelled
    # self.game_details = game_details # playoffs, nba finals, or regular season, to be labelled
    # self.opponent = opponent # opposing team, to be labelled
    # self.duration = duration # duration of clip, to be labelled


def get_video(payer_name, signature_move):
    search_query = f'{payer_name} {signature_move} game highlights'

    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY)

    request = youtube.search().list(
        part="id,snippet",
        type="video",
        q=search_query,
        videoDefinition='any',
        maxResults=25
    )
    try:
        response = request.execute()
        if not response:
            print("No response received.")
        else:
            videos_data = []
            for item in response.get("items", []):
               video_id = item.get("id", {}).get("videoId")
               upload_date = (item.get("snippet", {}).get("publishTime"))
               video_url = f'https://www.youtube.com/watch?v={video_id}'

               if video_id and upload_date:
                    parsed_datetime = datetime.fromisoformat(upload_date).strftime("%Y-%m-%d %H:%M:%S %z")
                    video = VideoData(video_id=video_id, upload_date=parsed_datetime, video_url=video_url)
                    videos_data.append(video) 
    except Exception as err:
        print(f"An error ocurred: {err}")
    
    for video in videos_data:
        videos_dict = {"video_id": video.video_id, 
                    "upload_date": video.upload_date, 
                    "video_url": video.video_url
                    }

    return videos_dict

def save_video(videos):
    df = pd.DataFrame(videos)
    df.rename_axis('ID', inplace=True)
    df.to_csv("kobe_videos.csv")

   
# TODO create pandas dataframe for video data and write to csv file
signature_moves = ["fadeaway", "3 pointer", "dunk", "layup", "clutch shot", "post Move", "crossover"]
videos_data = []
for sig in signature_moves:
    videos = get_video("kobe bryant", sig)
    videos_data.append(videos)

save_video(videos_data)







