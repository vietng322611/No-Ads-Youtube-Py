from UrlHandler import ytdl
from UrlHandler import get_video_info

import cv2
import numpy as np
import subprocess
import os

def condition(choose, i, num):
    if num == 1:
        if choose == 'n':
            i += 1
            os.system('cls')
            return i
        elif choose == 'q':
            exit(1)
    elif num == 2:
        if choose == 'p':
            i -= 1
            os.system('cls')
            return i
        elif choose == 'q':
            exit(1)

def get_user_input():
    url = input("Search something: ")
    if url == "quit" or url == "exit" or url == "q":
        return
    if url.startswith("https://www.youtube.com") or url.startswith("https://youtu.be"):
        video, title, thumbnail = ytdl(url, False)
    else:
        url, title, thumbnail = get_video_info(url)
    for i in range(len(title) // 10):
        print('\n'.join(title[i * 10:i * 10 + 10]))
        print('\nEnter number from 1 to 10 to choose a song.')
        if i  == len(title) // 10:
            print("p for previous page, q for exit.")
            choose = input("Your choose: ", end='')
            num = 1
            i = condition(choose, i, num)
        elif i == 0:
            print("n for next page, q for exit.")
            choose = input("Your choose: ", end='')
            num = 2
            i = condition(choose, i, num)
        else:
            print("p for previous page, n for next page, q for exit.")
            choose = input("Your choose: ", end='')
            i = condition(choose, i, 1)
            i = condition(choose, i, 2)
        while choose.isdigit() == False and choose != 'p' and choose != 'n' and choose != 'q':
            print("Your choose is invalid, please enter a number from 1 to 10.")
            choose = input("Your choose: ")
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
            elif choose.isdigit():
                if 0 <= int(choose) <= 9:
                    video = ytdl(url[i*10 + int(choose) - 1], True)
                    title = title[i*10 + int(choose) - 1]
                    return play(video, title)

def play(video, title):
    width = 1280
    height = 1024

    command = ['ffplay', '-i', video, '-window_title', title, '-filter:a "volume=0.2"', '-c:a pcm_f32le', '-autoexit']
    p1 = subprocess.Popen(command, stdout=subprocess.PIPE)
    while True:
        raw_frame = p1.stdout.read(width*height*3)
        if len(raw_frame) != (width*height*3):
            break
        frame = np.fromstring(raw_frame, np.uint8)
        frame = frame.reshape((height, width, 3))
        cv2.imshow('frame', frame)
        if cv2.waitKey(1):
            if 0xFF == ord('v'):
                vol = input("Enter a number from 0 to 100: ")
            elif 0xFF == ord('p'):
                print("Video paused.")
            elif 0xFF == ord('q'):
                print("Video stopped.")
                break
    try:
        p1.wait(1)
    except (subprocess.TimeoutExpired):
        p1.terminate()
    cv2.destroyAllWindows()
    os.system('cls')
    return get_user_input()

if __name__ == "__main__":
    get_user_input()