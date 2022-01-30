from email.mime import audio
from youtube_dl import YoutubeDL as youtubedl
from bs4 import BeautifulSoup as bs

import requests
import re

def get_video_info(url):
    r = requests.get(url)
    s = bs(r.text, "html.parser")
    title = s.find('title').get_text().replace(' - YouTube', '')
    return title

def ytdl(url):
    ydl_opts = {
        'agelimit': '20',
        'default_search': 'auto',
    }
    with youtubedl(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        for i in info['formats']:
            if i['ext'] == 'mp4':
                video = i['url']
        title = info['title'] 
        thumbnail = info['thumbnail']
    return video, title, thumbnail

def request(input):
    r = requests.get("https://www.youtube.com/results?search_query=" + input)
    s = bs(r.text, "html.parser")
    res = re.findall(r"watch\?v=(\S{11})", s.decode())
    return res