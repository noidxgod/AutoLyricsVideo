from PIL import ImageFont, ImageDraw, Image
import cv2
import moviepy.editor as mp
import numpy as np
import shutil
import math
img1 = cv2.imread('1.png')
with open('text.txt', 'r') as f:
    lines = f.read().splitlines()
for i in range(0,len(lines)):
    lines[i] = lines[i].replace("ё","е")
times = []
lyrics = []
x = 0
for i in range(0,len(lines)):
    if lines[i] == " ":
        x+=1
    else:
        lines[i] = lines[i].replace("[","")
        lines[i] = lines[i].split("]")
        times.append(lines[i][0])
        lyrics.append(lines[i][1])
for i in range(0,x):
    lines.remove(' ')
for i in range(0,len(times)):
    times[i] = times[i].replace(":",".0:")
    times[i] = times[i].split(":")
    times[i] = math.floor(float(times[i][0])*60 + float(times[i][1]))
#print(times)
writer = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 24,(1920,1080))#MJPG
print("Введите время в секундах:")
time = int(input())*24
times.append(time)
font = cv2.FONT_HERSHEY_COMPLEX
j = 0

for frame in range(time):
    print('\r', 'Процесс', str(frame * 100 // time), '%', end='')
    if (frame==times[j+1]*24):
        j += 1
    if (frame>=(times[j]*24) and frame < (times[j+1]*24)):
        shutil.copyfile('1.png', 'buffer1.png')
        shutil.copyfile('1.png', 'buffer2.png')
        try:
            img2 = cv2.imread('buffer1.png')
        except:
            img2 = cv2.imread('buffer2.png')
        cv2_im_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im_rgb)
        draw = ImageDraw.Draw(pil_im)
        font = ImageFont.truetype("font1.otf", 24)
        draw.text((960-len(lyrics[j])*10, 540), lyrics[j], font=font)
        cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
        #cv2.putText(img2, lyrics[j], (960-len(lyrics[j])*10, 540), font, 1, color=(255, 255, 255), thickness=2)
        writer.write(cv2_im_processed)
    else:
        writer.write(img1)
print('\r', str(100), '%', end='')
writer.release()
try:
    audio = mp.AudioFileClip("music.mp3")
    video1 = mp.VideoFileClip("output.mp4")
    final = video1.set_audio(audio)
    final.write_videofile("output2.mp4")
except:
    print("error")