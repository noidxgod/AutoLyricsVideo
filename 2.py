import glob

symbol = ".\ ".replace(' ','')
file = glob.glob('./*.mp3')[0].replace(symbol,'').replace(".mp3",'')

print(file)