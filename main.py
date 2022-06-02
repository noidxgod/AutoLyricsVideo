from PIL import ImageFont, ImageDraw, Image
import cv2
import moviepy.editor as mp
import numpy as np
import shutil
import math
import glob
def findfiles(extension):
    path = "./*." + str(extension)
    symbol = ".\ ".replace(" ","")
    filename = glob.glob(path)[0].replace(symbol,"")
    return(filename)

first_png_file = findfiles('png')
img1 = cv2.imread(first_png_file)
with open(findfiles('txt'), 'r') as f:
    lines = f.read().splitlines()
for i in range(0,len(lines)):
    lines[i] = lines[i].replace("ё","е").upper()
times = []
lyrics = []
x = 0
for i in range(0,len(lines)):
    if lines[i] == " " or lines[i] == "":
        x+=1
    else:
        lines[i] = lines[i].replace("[","")
        lines[i] = lines[i].split("]")
        times.append(lines[i][0])
        lyrics.append(lines[i][1])
for i in range(0,x):
    try:
        lines.remove(' ')
    except:
        lines.remove('')
for i in range(0,len(times)):
    times[i] = times[i].replace(":",".0:")
    times[i] = times[i].split(":")
    times[i] = math.floor(float(times[i][0])*60 + float(times[i][1]))
nameoutputfile = str(input("Введите имя выходного файла: "))+".mp4"
writer = cv2.VideoWriter(nameoutputfile, cv2.VideoWriter_fourcc(*"mp4v"), 24,(1920,1080))#MJPG
time = int(input("Введите время в секундах: "))*24
times.append(time)
font = cv2.FONT_HERSHEY_COMPLEX
j = 0
font_size = int(input("Введите размер шрифта: "))
x = int(input("Введите расположение по ширине: "))
y = int(input("Введите расположение по высоте: "))
for frame in range(0,time):
    print('\r', 'Процесс', str(frame * 100 // time), '%', end='')
    if (frame==times[j+1]*24):
        j += 1
    if (frame>=(times[j]*24) and frame < (times[j+1]*24)):
        shutil.copyfile(first_png_file, 'buffer1.png')
        shutil.copyfile(first_png_file, 'buffer2.png')
        try:
            img2 = cv2.imread('buffer1.png')
        except:
            img2 = cv2.imread('buffer2.png')
        cv2_im_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im_rgb)
        draw = ImageDraw.Draw(pil_im)
        try:
            font = findfiles('ttf')
        except:
            font = findfiles('otf')
        font = ImageFont.truetype(font, font_size)
        draw.text((x, y), lyrics[j], font=font, anchor="ms", align="left")
        cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
        writer.write(cv2_im_processed)
    if (frame<(times[j]*24)):
        writer.write(img1)
print('\r', str(100), '%', end='')
writer.release()
try:
    audio = mp.AudioFileClip(findfiles('mp3'))
    video1 = mp.VideoFileClip(nameoutputfile)
    final = video1.set_audio(audio)
    final.write_videofile("result.mp4")
except:
    print("error")