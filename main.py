from UrlHandler import ytdl

import cv2
import numpy as np
import subprocess

url = input("Enter a YouTube URL: ")
video, title, thumbnail = ytdl(url)

width = 1080
height = 600


command = ['ffplay', '-i', video, '-window_title', title, '-volume', '10', '-autoexit']

p1 = subprocess.Popen(command, stdout=subprocess.PIPE)

while True:
    raw_frame = p1.stdout.read(width*height*3)

    if len(raw_frame) != (width*height*3):
        print('Error reading frame!!!')
        break

    frame = np.fromstring(raw_frame, np.uint8)
    frame = frame.reshape((height, width, 3))
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
try:
    p1.wait(1)
except (subprocess.TimeoutExpired):
    p1.terminate()

cv2.destroyAllWindows()