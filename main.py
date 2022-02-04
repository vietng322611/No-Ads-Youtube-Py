from UrlHandler import ytdl
from UrlHandler import get_video_info

import subprocess
import os

def condition(choose, i, num):
    if choose == 'n' and num != 1:
        i += 1
        os.system('cls')
    elif choose == 'p' and num != 2:
        i -= 1
        os.system('cls')
    elif choose == 'q':
        exit(1)
    return i

def get_user_input():
    url = input("Search something: ")
    if url == "quit" or url == "exit" or url == "q":
        return
    if url.startswith("https://www.youtube.com") or url.startswith("https://youtu.be"):
        video, title, thumbnail = ytdl(url, False)
        return play(video, title)
    url, title, thumbnail = get_video_info(url)
    for i in range(len(title) // 10):
        print('\n'.join(list(map(lambda x, y: str(x) + ': ' + y, range(1, 11), title[i * 10:i * 10 + 10]))))
        print('\nEnter a number from 1 to 10 to choose a song.')
        if i  == len(title) // 10:
            print("p for previous page, q for exit.")
            choose = input("Your choose: ")
            num = 2
            i = condition(choose, i, num)
        elif i == 0:
            print("n for next page, q for exit.")
            choose = input("Your choose: ")
            num = 1
            i = condition(choose, i, num)
        else:
            print("p for previous page, n for next page, q for exit.")
            choose = input("Your choose: ")
            i = condition(choose, i, 1)
            i = condition(choose, i, 2)
        if choose.isdigit == True:
            if 0 <= int(choose) <= 9:
                video = ytdl(url[i*10 + int(choose) - 1], True)
                title = title[i*10 + int(choose) - 1]
                return play(video, title)
        while True:
            if choose.isdigit() == False:
                if choose == 'p' and num != 1:
                    i -= 1
                    os.system('cls')
                    break
                elif choose == 'n' and num != 2:
                    i += 1
                    os.system('cls')
                    break
                elif choose == 'q':
                    exit(1)
            elif 1 <= int(choose) <= 10:
                video = ytdl(url[i*10 + int(choose) - 1], True)
                title = title[i*10 + int(choose) - 1]
                return play(video, title)
            print("Your choose is invalid, please enter a number from 1 to 10.")
            choose = input("Your choose: ")

def play(video, title):
    width = 1280
    height = 720
    command = ['ffplay', 
                '-i', video, 
                '-window_title', title, 
                '-autoexit', 
                '-volume', '15',
                '-vf', f'scale={width}:{height}',
                '-vf', 'setpts=PTS/30',]

    p1 = subprocess.Popen(command, stdout=subprocess.PIPE)
    while True:
        try:
            p1.wait(1)
        except (subprocess.TimeoutExpired):
            p1.terminate()
            os.system('cls')
            return get_user_input()

if __name__ == "__main__":
    get_user_input()
