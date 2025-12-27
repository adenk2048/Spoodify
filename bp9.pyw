import pygame
import time
import random
from datetime import datetime
from mutagen.mp3 import MP3
import tkinter as tk
pygame.init()
pygame.mixer.init()


r2 = open("1_wrapped.in","a")
r3 = open("1_wrapped2.in","a")


rand = False

#create screen
screen = pygame.display.set_mode((520, 300))
pygame.display.set_caption("SPOODIFY")
font = pygame.font.Font(None,30)
small_font = pygame.font.Font(None,24)

#get name
name = ''
done = False

name_input = pygame.Rect(30,100,460,50)
while not done:

    pygame.draw.rect(screen, (80,200,120), name_input)
    text_surface0 = small_font.render(name,True,(0,0,0))
    text_rect0 = text_surface0.get_rect(midleft = (name_input.left+10,name_input.centery))
    screen.blit(text_surface0,text_rect0)
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                done = True
            elif event.key == pygame.K_BACKSPACE:
                name = name[:-1]
            else:
                name += event.unicode

        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.flip()
                
r = open(name+'.in')
t = r.readlines()
for i in range(len(t)-1):
    t[i] = t[i][:-1]
    
screen.fill((0, 0, 0), name_input)

t_unshuffled = t
#create buttons

next_button = pygame.Rect(150,120,100,50)
loop_button = pygame.Rect(30,120,100,50)
pause_button = pygame.Rect(270,120,100,50)
now_playing_button = pygame.Rect(30,200,460,50)
shuffle_button = pygame.Rect(390,120,100,50)

#create other stuff
index = 0
loop = False
running = True
pause = False
pause_time = 0
last_play = time.time()
loop_dict = {False:(80,200,120),True:(60,180,100)}

#pre-rendering
text_surface = font.render("NEXT", True, (0, 0, 0))
text_surface2 = font.render("LOOP", True, (0,0,0))
text_surface3 = font.render("PAUSE",True,(0,0,0))
text_surface5 = font.render("SHUFFLE",True,(0,0,0))

text_rect = text_surface.get_rect(center=next_button.center)
text_rect2 = text_surface.get_rect(center=loop_button.center)
text_rect3 = text_surface.get_rect(center = pause_button.center)
text_rect5 = text_surface5.get_rect(midleft = (shuffle_button.left+4, shuffle_button.centery))

while running:

    #draw next button
    pygame.draw.rect(screen, (80,200,120), next_button)
    screen.blit(text_surface, text_rect)

    #draw loop button
    pygame.draw.rect(screen,loop_dict[loop] , loop_button)
    screen.blit(text_surface2, text_rect2)

    #draw pause button
    pygame.draw.rect(screen, (80,200,120), pause_button)
    screen.blit(text_surface3,text_rect3)
    
    #draw 'now playing' screen
    pygame.draw.rect(screen, (80,200,120), now_playing_button)
    text_surface4 = font.render("NOW PLAYING: "+t[index],True,(0,0,0))
    text_rect4 = text_surface.get_rect(midleft = (now_playing_button.left+10,now_playing_button.centery))
    screen.blit(text_surface4,text_rect4)

    #draw shuffle button
    pygame.draw.rect(screen, (80,200,120), shuffle_button)
    screen.blit(text_surface5,text_rect5)
    
    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            #next song
            
            if next_button.collidepoint(event.pos):
                
                pygame.mixer.stop()

                play_time = time.time()-last_play - pause_time
                r2.write(str(datetime.now())+" "+t[index]+
                         " "+str(play_time)+"\n")
                r3.write(t[index]+" "+str(play_time)+"\n")
                
                #print(pause_time)
                pause_time = 0
                pause = False
                
                index = (index + (not loop))%(len(t))
                if rand and not loop:
                    random.shuffle(t)
                    t.reverse()
                
                #print(t[index],MP3(t[index]+'.mp3').info.length)
                pygame.mixer.music.load(t[index]+".mp3")
                pygame.mixer.music.play()
                last_play = time.time()

            #boring functions
            if loop_button.collidepoint(event.pos):
                loop = not loop
                #print("loop setting: "+str(loop))

            if pause_button.collidepoint(event.pos):
                pause = not pause
                if pause:
                    last_pause = time.time()
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

            if shuffle_button.collidepoint(event.pos):
                rand = not rand
                if not rand:
                    t = t_unshuffled
                else:
                    random.shuffle(t)
                    t.reverse()
            
        if event.type == pygame.QUIT:
            running = False

    if not pygame.mixer.music.get_busy() and not pause:
        #auto play
        pygame.mixer.stop()

        song_length = MP3(t[index]+'.mp3').info.length
        r2.write(str(datetime.now())+" "
                 +t[index]+" "+str(song_length)+'\n')
        r3.write(t[index]+" "+str(song_length)+'\n')
        pause_time = 0
        index = (index + (not loop))%(len(t))
        
        if rand and not loop:
            random.shuffle(t)
            t.reverse()

        #print(t[index],MP3(t[index]+'.mp3').info.length)
        pygame.mixer.music.load(t[index]+".mp3")
        pygame.mixer.music.play()
        last_play = time.time()
        

    if pause:
        pause_time += time.time() - last_pause
        last_pause = time.time()

    if not rand:
        t = t_unshuffled
    
    pygame.display.flip()
    
pygame.quit()

play_time = time.time()-last_play - pause_time
r2.write(str(datetime.now())+" "+t[index]+
        " "+str(play_time)+"\n")
r3.write(t[index]+" "+str(play_time)+"\n")

r2.close()
r3.close()
