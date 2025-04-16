import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.youtube.com/feed/trending"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')

videos = soup.find_all('ytd-video-renderer')

video_data = []
for video in videos:
    title = video.find('a', {'id': 'video-title'})
    if title:
        title = title.get('title')
        url = 'https://www.youtube.com' + title.get('href')
        views = video.find('span', {"class": 'view-count'})
        views = views.text if views else 'N/A'
        video_data.append({
            'title': title,
            'url': url,
            'views': views
        })

df = pd.DataFrame(video_data)

df.to_csv('trending_videos.csv', index=False)

print(df)
