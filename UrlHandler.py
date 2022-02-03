from youtube_dl import YoutubeDL as youtubedl
from bs4 import BeautifulSoup as bs

import requests
import re

def get_video_info(input):
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
    r = requests.get("https://www.youtube.com/results", params={'search_query': input}, headers=headers)
    s = bs(r.text, 'html.parser')
    url = list(map(lambda x: "https://www.youtube.com/watch?v=" + x, re.findall(r"watch\?v=(\S{11})", str(s))))
    thumbnails = re.findall(r'"thumbnails":\[{"url":"(.*?)"', str(s))
    titles = re.findall(r'"title":{"runs":\[{"text":"(.+?)"', str(s))
    return url, titles, thumbnails

def ytdl(url, search):
    ydl_opts = {
        'agelimit': '20',
        'default_search': 'auto',
        'audio-format': 'wav',
        'quiet': 'True',
        'video_quality': '720p',
    }
    with youtubedl(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        for i in info['formats']:
            if i['ext'] == 'mp4':
                if i['acodec'] == 'mp4a.40.2':
                    video = i['url']
                    if search:
                        return video
        title = info['title'] 
        thumbnail = info['thumbnail']
    return video, title, thumbnail