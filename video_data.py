# Displays Video Metrics
# view count, like count, dislike count, comment count
# uses tabulate to display data on terminal

# next goal -> sort through videos with a specific person

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) #ignores future warning for using .append as opposed to .concat

import pandas as pd
import requests # makes API calls
import time
import json
from tabulate import tabulate

# youtube API key
API_KEY = 'AIzaSyCsl4Bsqd025UpmnjKifrO8xknTRDCh6kE'
CHANNEL_ID = 'UCfBIIJWYgTFHZW7B-nsVl4w'

# second api call
def get_video_details(video_id):
    url_video_stats = "https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&part=statistics&key="+API_KEY
    response_video_stats = requests.get(url_video_stats).json()

    view_count = response_video_stats['items'][0]['statistics']['viewCount']
    like_count = response_video_stats['items'][0]['statistics']['likeCount']
    comment_count = response_video_stats['items'][0]['statistics']['commentCount']

    return view_count, like_count, comment_count

# first api call
def get_videos(df):
    pageToken = ''
    url = "https://www.googleapis.com/youtube/v3/search?key="+API_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=date&maxResults=5"+pageToken
    response = requests.get(url).json()
    time.sleep(1)
    # grabs specific VALUE from json data
    video_id = response['items'][0]['id']['videoId']
    video_title = response['items'][0]['snippet']['title']
    upload_date = response['items'][0]['snippet']['publishedAt']
    upload_date = str(upload_date).split('T')[0] # gets just the date

    for video in response['items']:
        if video['id']['kind'] == 'youtube#video': # logic for picking out youtube videos
            video_id = video['id']['videoId']
            video_title = video['snippet']['title']
            upload_date = video['snippet']['publishedAt']
            upload_date = str(upload_date).split('T')[0] # gets just the date

            #second api call function
            view_count, like_count, comment_count = get_video_details(video_id)

            # save data in pandas df
            df = df.append({'video_id': video_id, 'video_title': video_title, 'upload_date': upload_date, 'view_count': view_count, 'like_count': like_count, 'comment_count': comment_count}, ignore_index=True)

            # TESTS for DATA
            # print(video_id)
            # print(video_title)
            # print(upload_date)
            # print(view_count)
            # print(like_count)
            # print(comment_count)
    return df

# build dataframe
df = pd.DataFrame(columns = ['video_id', 'video_title', 'upload_date', 'view_count', 'like_count', 'comment_count'])
df = get_videos(df)

# prints with pretty json in terminal
# print(json.dumps(response, indent=4))

print(tabulate(df, headers='keys', tablefmt='psql'))

# NOW SAVE df TO CSV FILE
# use csvkit in terminal for local SQL commands 
df.to_csv('stats.csv', index=False)
