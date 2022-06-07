from PIL import ImageFont, ImageDraw
from PIL import Image as Img
import cv2
import moviepy.editor as mp
import numpy as np
import shutil
import math
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import pyglet
from tkinter import *
from tkinter.ttk import Progressbar  
from tkinter import messagebox 

root = tk.Tk()
root.title('Lyrics')
root.minsize(700, 235)
root.maxsize(1500, 235)
root.geometry("150x100")
#root.rowconfigure([0,1,2,3,4,5,6], minsize=25,weight=1)
#root.columnconfigure([0,1],minsize=200,weight=1)
#root.resizable(False, False)

style = ttk.Style()  
label_progress_bar = Label(root, text='') 
def btn_background():
    global text_background
    try:
        label_background.after(1000, label_background.destroy())
    except:
        text_background = fd.askopenfilename(title='Открыть файл фона(png)',initialdir='/')
        label_background = Label(root, text=text_background)    
        label_background.grid(column=1, row=0,sticky=W,ipadx=10,ipady=2) 

def btn_lyrics():
    global text_lyrics
    try:
        label_lyrics.after(1000, label_lyrics.destroy())
    except:
        text_lyrics = fd.askopenfilename(title='Открыть файл с текстом песни(txt)',initialdir='/')
        label_lyrics = Label(root, text=text_lyrics)    
        label_lyrics.grid(column=1, row=1,sticky=W,ipadx=10,ipady=2) 

def btn_music():
    global text_music
    try:
        label_music.after(1000, label_music.destroy())
    except:
        text_music = fd.askopenfilename(title='Открыть файл с музыкой(mp3)',initialdir='/')
        label_music = Label(root, text=text_music)    
        label_music.grid(column=1, row=2,sticky=W,ipadx=10,ipady=2) 

def btn_font():
    global text_font
    try:
        label_font.after(1000, label_font.destroy())
    except:
        text_font = fd.askopenfilename(title='Открыть файл шрифта(ttf,otf)',initialdir='/')
        label_font = Label(root, text=text_font)    
        label_font.grid(column=1, row=3,sticky=W,ipadx=10,ipady=2) 

def btn_output_folder():
    global text_output_folder
    try:
        label_output_folder.after(1000, label_output_folder.destroy())
    except:
        text_output_folder = fd.askdirectory(title='Открыть папку',initialdir='/')
        label_output_folder = Label(root, text=text_output_folder)
        label_output_folder.grid(column=1, row=4,sticky=W,ipadx=10,ipady=2)

def loading(text_loading):
    label_output_folder = Label(root, text=text_loading)
    label_output_folder.grid(column=1, row=6,sticky=W,ipadx=10,ipady=2)g

def start():
    img1 = cv2.imread(text_background)
    print(text_lyrics)
    with open(text_lyrics, 'r') as f:
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
    nameoutputfile = "result.mp4" #str(input("Введите имя выходного файла: "))
    writer = cv2.VideoWriter(text_output_folder + '/' + nameoutputfile, cv2.VideoWriter_fourcc(*"mp4v"), 24,(1920,1080))#MJPG
    song = pyglet.media.load(text_music)
    time = int(song.duration)*24#int(time_input.get())#148#int(input("Введите время в секундах: "))*24
    #times.append(time)
    times.append(time)
    print(times)
    #
    font = cv2.FONT_HERSHEY_COMPLEX
    j = 0
    print(times[len(times)-2]*24+3*24)
    #font_size = int(input("Введите размер шрифта: "))7
    x = 960#int(input("Введите расположение по ширине: "))
    y = 140#int(input("Введите расположение по высоте: "))
    loading("Создание видео..")
    for frame in range(0,time):
        if int(frame * 100 // time) % 2 == 0:
            Tk.update(root)  
        pb['value'] =  int(frame * 100 // time)
        #messagebox.showinfo()   
        if (frame==times[j+1]*24):
            j += 1
        if (frame>=(times[len(times)-2]*24+3*24)):
            writer.write(img1)
        elif (frame>=(times[j]*24)):
            shutil.copyfile(text_background, 'buffer1.png')
            shutil.copyfile(text_background, 'buffer2.png')
            try:
                img2 = cv2.imread('buffer1.png')
            except:
                img2 = cv2.imread('buffer2.png')
            cv2_im_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
            pil_im = Img.fromarray(cv2_im_rgb)
            draw = ImageDraw.Draw(pil_im)
            font = ImageFont.truetype(text_font, int(font_size_input.get()))
            draw.text((x, y), lyrics[j], font=font, anchor="ms", align="left")
            cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
            writer.write(cv2_im_processed)
        else:
            writer.write(img1)
    pb['value'] = 100
    writer.release()
    if (chk_state==True):
        loading("Добавление музыки в видео..")
        try:
            audio = mp.AudioFileClip(text_music)
            video1 = mp.VideoFileClip(text_output_folder + '/' + nameoutputfile)
            final = video1.set_audio(audio)
            final.write_videofile(text_output_folder + '/' + "result_with_music.mp4")
        except:
            loading("Ошибка добавлении музыки")
        loading("Готово!")
    else:
        loading("Готово!")
button_background = tk.Button(master = root,text='Открыть файл фона(png)',command=btn_background,width=30)
button_lyrics = tk.Button(master = root,text='Открыть файл с текстом песни(txt)',command=btn_lyrics,width=30)
button_music = tk.Button(master = root,text='Открыть файл с музыкой(mp3)',command=btn_music,width=30)
button_font = tk.Button(master = root,text='Открыть файл шрифта(ttf,otf)',command=btn_font,width=30)
button_output_folder = tk.Button(master = root,text='Открыть папку сохранения',command=btn_output_folder,width=30)
button_start = tk.Button(master = root, text = 'Старт',command = start,width=30)
font_size_input  = Entry(master = root,width=21)
label_font_size_input = Label(master = root, text="Размер шрифта",width=30) 
pb = ttk.Progressbar(root,orient='horizontal',mode='determinate',length=130)

button_background.grid(column=0, row=0,sticky=W, ipadx=10,ipady=2) 
button_lyrics.grid(column=0, row=1,sticky=W, ipadx=10,ipady=2) 
button_music.grid(column=0, row=2,sticky=W, ipadx=10,ipady=2) 
button_font.grid(column=0, row=3,sticky=W, ipadx=10,ipady=2) 
button_output_folder.grid(column=0, row=4,sticky=W, ipadx=10,ipady=2)
label_font_size_input.grid(column=0,row = 5,sticky=W, ipadx=10,ipady=2)
font_size_input.grid(column=1, row=5,sticky=W, padx=10,ipady=2)
button_start.grid(column=0,row=7,sticky=W, ipadx=10,ipady=2)
pb.grid(column=1,row=7,sticky=W,padx=10,ipady=2)

chk_state = BooleanVar()  
chk_state.set(True)  # задайте проверку состояния чекбокса  
chk = Checkbutton(root, text='Добавить музыку?', var=chk_state)  
chk.grid(column=0, row=6) 

root.mainloop()