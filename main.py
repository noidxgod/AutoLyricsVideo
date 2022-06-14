from PIL import ImageFont, ImageDraw
from PIL import Image as Img
import os
import cv2
import moviepy.editor as mp
import numpy as np
import shutil
import math
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import *
from tkinter.ttk import Progressbar  
from tkinter import messagebox as mb

root = tk.Tk()
root.title('Lyrics')
root.minsize(700, 300)
root.maxsize(1500, 300)
root.geometry("150x100") 
#root.rowconfigure([0,1,2,3,4,5,6], minsize=25,weight=1)
#root.columnconfigure([0,1],minsize=200,weight=1)
#root.resizable(False, False)
def btn_background():
    global text_background
    global label_background 
    try:
        label_background.after(1000, label_background.destroy())
    except:
        print()
    text_background = fd.askopenfilename(filetypes=[("PNG", ".png")],title='Открыть файл фона(png,jpg)',initialdir='/')
    label_background  = Label(root, text=text_background)    
    label_background.grid(column=1, row=0,sticky=W,ipadx=10,ipady=2) 
def btn_lyrics():
    global text_lyrics
    global label_lyrics
    try:
        label_lyrics.after(1000, label_lyrics.destroy())
    except:
        print()
    text_lyrics = fd.askopenfilename(filetypes=[("TXT files", ".txt")],title='Открыть файл с текстом песни(txt)',initialdir='/')
    label_lyrics = Label(root, text=text_lyrics)    
    label_lyrics.grid(column=1, row=1,sticky=W,ipadx=10,ipady=2) 
def btn_music():
    global text_music
    global label_music
    try:
        label_music.after(1000, label_music.destroy())
    except:
        print()
    text_music = fd.askopenfilename(filetypes=[("MP3 files", ".mp3")],title='Открыть файл с музыкой(mp3)',initialdir='/')
    label_music = Label(root, text=text_music)    
    label_music.grid(column=1, row=2,sticky=W,ipadx=10,ipady=2) 
def btn_font():
    global text_font
    global label_font
    try:
        label_font.after(1000, label_font.destroy())
    except:
        print()
    text_font = fd.askopenfilename(filetypes=[("TTF, OTF", ".ttf .otf")],title='Открыть файл шрифта(ttf,otf)',initialdir='/')
    label_font = Label(root, text=text_font)    
    label_font.grid(column=1, row=3,sticky=W,ipadx=10,ipady=2) 
def btn_output_folder():
    global text_output_folder
    global label_output_folder
    try:
        label_output_folder.after(1000, label_output_folder.destroy())
    except:
        print()
    text_output_folder = fd.askdirectory(title='Открыть папку',initialdir='/')
    label_output_folder = Label(root, text=text_output_folder)
    label_output_folder.grid(column=1, row=4,sticky=W,ipadx=10,ipady=2)


def loading(text_loading):
    global label_progress_bar
    try:
        label_progress_bar.after(1000, label_progress_bar.destroy())
    except:
        print()
    label_progress_bar = Label(root, text=text_loading)
    label_progress_bar.grid(column=1, row=11,sticky=W,ipadx=10,ipady=2)

def start():
    Tk.update(root) 
    if 'text_background'  in globals() and 'text_font' in globals() and 'text_lyrics' in globals() and 'text_output_folder' in globals():
        if (text_background != '' and text_font != ''  and text_lyrics != '' and text_output_folder != ''):
            
            img1 = cv2.imread(text_background)
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

            try:
                time = int(time_input.get())*24
            except:
                mb.showerror("Ошибка","Введите длину видео в секундах")

            times.append(time)
            font = cv2.FONT_HERSHEY_COMPLEX
            j = 0
            #font_size = int(input("Введите размер шрифта: "))7


        
            try:
                x = int(x_input.get())# 960#int(input("Введите расположение по ширине: "))
                y = int(x_input.get())#140#int(input("Введите расположение по высоте: "))
            except: 
                x = -1
                y = -1
                mb.showerror("Ошибка","Введите расположение текста")

            if (x > 0 and y > 0):
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
                        shutil.copyfile(text_background, text_output_folder + '/' + 'buffer1.png')
                        shutil.copyfile(text_background, text_output_folder + '/' + 'buffer2.png')
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
                os.remove(text_output_folder + '/' + 'buffer1.png')
                os.remove(text_output_folder + '/' + 'buffer2.png')
                if 'text_music'  in globals():
                    loading("Добавление музыки в видео..")
                    if (text_music != ''):
                        try:
                            audio = mp.AudioFileClip(text_music)
                            video1 = mp.VideoFileClip(text_output_folder + '/' + nameoutputfile)
                            final = video1.set_audio(audio)
                            final.write_videofile(text_output_folder + '/' + "result_with_music.mp4")
                        except:
                            mb.showerror("Ошибка","Музыка не добавилась")
                        loading("Готово!")
                else:
                    loading("Готово!")
        else:
            mb.showerror("Ошибка","Выбраны не все файлы")
    else: 
        mb.showerror("Ошибка","Выбраны не все файлы")       

button_background = tk.Button(master = root,text='Открыть файл фона(png)',command=btn_background,width=30)
button_lyrics = tk.Button(master = root,text='Открыть файл с текстом песни(txt)',command=btn_lyrics,width=30)
button_music = tk.Button(master = root,text='Открыть файл с музыкой(mp3)',command=btn_music,width=30)
button_font = tk.Button(master = root,text='Открыть файл шрифта(ttf,otf)',command=btn_font,width=30)
button_output_folder = tk.Button(master = root,text='Открыть папку сохранения',command=btn_output_folder,width=30)
button_start = tk.Button(master = root, text = 'Старт',command = start,width=30)
font_size_input  = Entry(master = root,width=5)
label_font_size_input = Label(master = root, text="Размер шрифта",width=30) 
label_time_input = Label(master = root, text="Длина ролика в секундах",width=30) 
label_x_input = Label(master = root, text="Расположение текста по ширине",width=30)
label_y_input = Label(master = root, text="Расположение текста по высоте",width=30)
pb = ttk.Progressbar(root,orient='horizontal',mode='determinate',length=130)

button_background.grid(column=0, row=0,sticky=W, ipadx=10,ipady=2) 
button_lyrics.grid(column=0, row=1,sticky=W, ipadx=10,ipady=2) 
button_music.grid(column=0, row=2,sticky=W, ipadx=10,ipady=2) 
button_font.grid(column=0, row=3,sticky=W, ipadx=10,ipady=2) 
button_output_folder.grid(column=0, row=4,sticky=W, ipadx=10,ipady=2)
label_font_size_input.grid(column=0,row = 6,sticky=W, ipadx=10,ipady=2)
font_size_input.grid(column=1, row=6,sticky=W, padx=10,ipady=2)
label_time_input.grid(column=0,row=7,sticky=W, ipadx=10,ipady=2)
label_x_input.grid(column=0,row=8,sticky=W, ipadx=10,ipady=2)
label_y_input.grid(column=0,row=9,sticky=W, ipadx=10,ipady=2)
button_start.grid(column=0,row=10,sticky=W, ipadx=10,ipady=2)
pb.grid(column=1,row=10,sticky=W,padx=10,ipady=2)



time_input  = Entry(master = root,width=5)
time_input.grid(column=1, row=7,sticky=W, padx=10,ipady=2)

x_input  = Entry(master = root,width=5)
x_input.grid(column=1, row=8,sticky=W, padx=10,ipady=2)

y_input  = Entry(master = root,width=5)
y_input.grid(column=1, row=9,sticky=W, padx=10,ipady=2)

root.mainloop()