import os
import requests
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

api_key = os.getenv('YOUTUBE_API_KEY')

url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=US&key={api_key}'

response = requests.get(url)
  
if response.status_code == 200:
    data = response.json()

    video_data = []
    for item in data['items']:
        title = item['snippet']['title']
        video_url = f'https://www.youtube.com/watch?v={item["id"]}'
        views = item['statistics'].get('viewCount', 'N/A')
        likes = item['statistics'].get('likeCount', 'N/A')  
        video_data.append({
            'title': title,
            'url': video_url,
            'views': views,
            'likes': likes
        })

    df = pd.DataFrame(video_data)
    df.to_csv('trending_videos.csv', index=False)

    print(df)
else:
    print(f"Failed to fetch data. HTTP status code: {response.status_code}")
