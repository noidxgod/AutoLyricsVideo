import pyglet
song = pyglet.media.load('test.mp3')
print(int(song.duration))