import matplotlib
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg

import librosa
import librosa.display
import IPython.display
import numpy as np



import pylab

fig = pylab.figure(figsize=[4, 4], # Inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                   )
ax = fig.gca()
#ax.plot([1, 2, 4])


import pygame
from pygame.locals import *

sndfile= 'shorter.wav'
import sys

y, sr = librosa.load(sndfile)
maxv = np.iinfo(np.int16).max
print(y.shape)
print(sr)
print(y)
print(y)
#sys.exit()

D = librosa.stft(y)

# Separate the magnitude and phase
S, phase = librosa.magphase(D)

# Decompose by nmf
components, activations = librosa.decompose.decompose(S, n_components=8, sort=True)

#plt.figure(figsize=(12,4))

#ax.subplot(1,2,2)
librosa.display.specshow(activations, x_axis='time')
ax.set_xlabel('Time')
ax.set_ylabel('Component')
ax.set_title('Activations')
#ax.tight_layout()

canvas = agg.FigureCanvasAgg(fig)
canvas.draw()
renderer = canvas.get_renderer()
raw_data = renderer.tostring_rgb()

yarray_k = []

for k in range(0,8):
    # Resynthesize.  How about we isolate just first (lowest) component?

    # Reconstruct a spectrogram by the outer product of component k and its activation
    D_k = np.multiply.outer(components[:, k], activations[k])

    # invert the stft after putting the phase back in
    y_k = librosa.istft(D_k * phase)

    # And playback
    print('Component #{}'.format(k))
    yk = (y_k*maxv).astype(np.int16)
    yarray_k.append(yk)

# Resynthesize.  How about we isolate a middle-frequency component?
#k = len(activations) // 2
k = 1

# Reconstruct a spectrogram by the outer product of component k and its activation
D_k = np.multiply.outer(components[:, k], activations[k])

# invert the stft after putting the phase back in
y_k = librosa.istft(D_k * phase)

# And playback
print('Component #{}'.format(k))




y = (y*maxv).astype(np.int16)
#pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
pygame.mixer.pre_init(frequency=sr, size=-16, channels=1, buffer=4096)
print (pygame.mixer.get_init() )




pygame.init()

window = pygame.display.set_mode((400, 400), DOUBLEBUF)
screen = pygame.display.get_surface()

size = canvas.get_width_height()

surf = pygame.image.fromstring(raw_data, size, "RGB")
screen.blit(surf, (0,0))
pygame.display.flip()

blue=(0,0,255)

s = pygame.mixer.Sound(sndfile)
snd_length=s.get_length()*1000
print("length",snd_length)

#pygame.mixer.Sound(y).play()
sound_object = pygame.sndarray.make_sound(y)
sound_object.play()


#s = pygame.mixer.music.load(sndfile)
#s = pygame.mixer.music.load(sound_object)
#pygame.mixer.music.play()
#ch = s.play()

x = 0
start = pygame.time.get_ticks()
crashed = False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            sound_object.stop()
            start = pygame.time.get_ticks()
            if event.key == pygame.K_0:
                sound_object = pygame.sndarray.make_sound(yarray_k[0])
                sound_object.play()
            if event.key == pygame.K_1:
                print("keydown 1")
                sound_object = pygame.sndarray.make_sound(yarray_k[1])
                sound_object.play()
            elif event.key == pygame.K_2:
                sound_object = pygame.sndarray.make_sound(yarray_k[2])
                sound_object.play()
                print("keydown 2")
            elif event.key == pygame.K_3:
                sound_object = pygame.sndarray.make_sound(yarray_k[3])
                sound_object.play()
                print("keydown 3")
            elif event.key == pygame.K_4:
                sound_object = pygame.sndarray.make_sound(yarray_k[4])
                sound_object.play()
                print("keydown 4")
            elif event.key == pygame.K_5:
                sound_object = pygame.sndarray.make_sound(yarray_k[5])
                sound_object.play()
                print("keydown 5")
            elif event.key == pygame.K_6:
                sound_object = pygame.sndarray.make_sound(yarray_k[6])
                sound_object.play()
                print("keydown 6")
            elif event.key == pygame.K_7:
                sound_object = pygame.sndarray.make_sound(yarray_k[7])
                sound_object.play()
                print("keydown 7")
            elif event.key == pygame.K_a:
                sound_object = pygame.sndarray.make_sound(y)
                sound_object.play()
                print("keydown A")
    # draw here
    screen.blit(surf, (0,0))
    #print(pygame.mixer.music.get_pos())
    location = ((pygame.mixer.music.get_pos()/snd_length))
    #print((pygame.mixer.music.get_pos()/snd_length))
    #print(location)
    #print(x)
    x =( pygame.time.get_ticks() - start) 
    x = x / snd_length
    #print(x)
    buffer = 90
    x = x*(400-buffer)
    x = x + buffer/2+10
    #print(x)
    pygame.draw.rect(window,blue,(int(x),0,5,400))
    pygame.display.update()
    #print(pygame.time.get_ticks())

    #clock.tick(60)
