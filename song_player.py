import pygame
import time
import random
from mutagen.mp3 import MP3
from datetime import datetime
pygame.init()
pygame.mixer.init()

print("Welcome to Spoodify")
#open playlist .in file
name = input('name of playlist (do not put .txt)')
rand = input('Shuffle? (y/n)')

if rand == 'y':
    rand = True

r = open(name+'.txt')
t = r.readlines()
for i in range(len(t)-1):
    t[i] = t[i][:-1]

r2 = open("song_history.txt","a")
r3 = open("song_plays.txt","a")

#create screen
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("SPOODIFY")
font = pygame.font.Font(None,30)

#create buttons
next_button = pygame.Rect(150,120,100,50)
loop_button = pygame.Rect(30,120,100,50)

#create other stuff
index = 0
loop = False
last_play = time.time()
running = True
interval = 0#MP3(t[index]+'.mp3').info.length

while running:

    #draw next button
    pygame.draw.rect(screen, (80,200,120), next_button)
    text_surface = font.render("NEXT", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=next_button.center)
    screen.blit(text_surface, text_rect)

    #draw loop button
    pygame.draw.rect(screen, (80,200,120), loop_button)
    text_surface2 = font.render("LOOP", True, (0,0,0))
    text_rect2 = text_surface.get_rect(center=loop_button.center)
    screen.blit(text_surface2, text_rect2)
    
    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if next_button.collidepoint(event.pos):
                pygame.mixer.stop()
                r2.write(str(datetime.now())+" "+t[index]+
                         " "+str(time.time() - last_play)+"\n")
                r3.write(t[index]+" "+str(time.time() - last_play)+"\n")
                
                index = (index + (not loop))%(len(t))
                if rand and not loop:
                    random.shuffle(t)
                interval = MP3(t[index]+'.mp3').info.length
                print(t[index], MP3(t[index]+'.mp3').info.length)
                pygame.mixer.music.load(t[index]+".mp3")
                pygame.mixer.music.play()
                last_play = time.time()

                
            if loop_button.collidepoint(event.pos):
                loop = not loop
                print("loop setting: "+str(loop))
        if event.type == pygame.QUIT:
            running = False

    if time.time() - last_play >= interval:
        pygame.mixer.stop()
        r2.write(str(datetime.now())+" "+t[index]+
                         " "+str(interval)+"\n")
        r3.write(t[index]+" "+str(interval)+"\n")
        index = (index + (not loop))%(len(t))
        
        if rand and not loop:
            random.shuffle(t)
        
        interval = MP3(t[index]+'.mp3').info.length
        print(t[index], MP3(t[index]+'.mp3').info.length)
        pygame.mixer.music.load(t[index]+".mp3")
        pygame.mixer.music.play()
        last_play = time.time()
        
        
    pygame.display.flip()
    
pygame.quit()

r2.write(str(datetime.now())+" "+t[index]+
        " "+str(time.time() - last_play)+"\n")
r3.write(t[index]+" "+str(time.time() - last_play)+"\n")
r2.close()
r3.close()

