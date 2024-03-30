# Implementing Songs into game
# Required : Song-Lyrics Callibration Mode
# 10-4-23
# Version 3

import pygame
from pygame import mixer
import random
import numpy as np
import os

pygame.init()
sc_w, sc_h = 500, 700
wn = pygame.display.set_mode((sc_w, sc_h))
pygame.display.set_caption("Type Warrior")
clock = pygame.time.Clock()

# Background Music
mixer.music.load("bg_music.mp3")
mixer.music.play(-1)

# Get Word Bank
dictionary = []
with open("easy_word.txt") as f:
    for line in f:
        dictionary.append(line.strip())
f.close()

score = 0
multiplier = 1

def menu(wn):
    buttons = [Button([sc_w / 2, 3*sc_h / 5], [sc_w/2, 70], [30, 30, 30], [60, 60, 60], "Endless", [200, 200, 200], endless),
               Button([sc_w / 2, 3*sc_h / 5 + 90], [sc_w/2, 70], [30, 30, 30], [60, 60, 60], "Lyrics Race", [200, 200, 200], song_menu),
               Button([sc_w / 2, 3*sc_h / 5 + 180], [sc_w/2, 70], [30, 30, 30], [60, 60, 60], "Callibration", [200, 200, 200], callibrate_menu),
               Button([sc_w / 2, 3*sc_h / 5 + 270], [sc_w/2, 70], [30, 30, 30], [60, 60, 60], "Test Zone", [200, 200, 200], testing)]
    while True:
        wn.fill((0, 0, 0))
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.highlighted:
                        select = mixer.Sound("ButtonSelect.wav")
                        select.play()
                        button.func(wn)

        # Title
        font = pygame.font.SysFont("Ariel", 90)
        text = font.render("Type Warrior", 1, (255, 255, 255))
        wn.blit(text, (sc_w / 2 - text.get_width() / 2, 30))
        font = pygame.font.SysFont("Ariel", 20)
        version = font.render("Version 3", 1, (100, 100, 100))
        wn.blit(version, (sc_w - version.get_width(), 4))

        # Graphics
        rad = 100
        pygame.draw.line(wn, (255, 255, 255), (int(sc_w /2), 230), (int(sc_w/2 + rad*np.cos(np.deg2rad(270 + 140))), int(230 - rad*np.sin(np.deg2rad(270 + 140)))), 5)
        pygame.draw.line(wn, (255, 255, 255), (int(sc_w /2), 230), (int(sc_w/2 + rad*np.cos(np.deg2rad(270 - 140))), int(230 - rad*np.sin(np.deg2rad(270 - 140)))), 5)
        pygame.draw.line(wn, (255, 255, 255), (int(sc_w/2 + rad*np.cos(np.deg2rad(270))), int(230 - rad*np.sin(np.deg2rad(270)))), (int(sc_w/2 + rad*np.cos(np.deg2rad(270 + 140))), int(230 - rad*np.sin(np.deg2rad(270 + 140)))), 5)
        pygame.draw.line(wn, (255, 255, 255), (int(sc_w/2 + rad*np.cos(np.deg2rad(270))), int(230 - rad*np.sin(np.deg2rad(270)))), (int(sc_w/2 + rad*np.cos(np.deg2rad(270 - 140))), int(230 - rad*np.sin(np.deg2rad(270 - 140)))), 5)

        # Buttons
        for button in buttons:
            button.update(wn)

        pygame.display.update()

def endless(wn):
    global score, multiplier
    old_keys = pygame.key.get_pressed()
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    enemies = []
    bullets = []
    booms = []
    engaged_with = None
    hearts = 6
    wave = 0
    count = 1
    game_over = False
    buttons = []

    # Player Attributes
    rad = 20
    dir = 90
    pos = [int(sc_w / 2), int(8*sc_h / 9)]
    
    while True:
        wn.fill((0, 0, 0))
        clock.tick(60)
        count += 1

        # Wave Management
        if count < 150:
            font = pygame.font.SysFont("Ariel", 50)
            text = font.render("Endless Mode", 1, (255, 255, 255))
            wn.blit(text, (sc_w / 2 - text.get_width() / 2, 100))
        elif count == 150:
            wave += 1
        
        if count % 1500 == 0:
            wave += 1

        # Clicking Actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.highlighted:
                        select = mixer.Sound("ButtonSelect.wav")
                        select.play()
                        button.func(wn)

        # Detect Keys
        if not game_over:
            old_keys, new_c, Enter, BackSpace = keyboard_detection(old_keys)
            if new_c != "":
                if engaged_with is None:
                    for enemy in enemies:
                        if enemy.word[0] == new_c[0]:
                            enemy.engaged = True
                            engaged_with = enemy
                            for letter in new_c:
                                engaged_with.attack(letter, bullets, booms)
                else:
                    for letter in new_c:
                        engaged_with.attack(letter, bullets, booms)

        # Player
        pygame.draw.line(wn, (255, 255, 255), (pos[0], pos[1]), (int(pos[0] + rad*np.cos(np.deg2rad(dir + 140))), int(pos[1] - rad*np.sin(np.deg2rad(dir + 140)))), 1)
        pygame.draw.line(wn, (255, 255, 255), (pos[0], pos[1]), (int(pos[0] + rad*np.cos(np.deg2rad(dir - 140))), int(pos[1] - rad*np.sin(np.deg2rad(dir - 140)))), 1)
        pygame.draw.line(wn, (255, 255, 255), (int(pos[0] + rad*np.cos(np.deg2rad(dir))), int(pos[1] - rad*np.sin(np.deg2rad(dir)))), (int(pos[0] + rad*np.cos(np.deg2rad(dir + 140))), int(pos[1] - rad*np.sin(np.deg2rad(dir + 140)))), 1)
        pygame.draw.line(wn, (255, 255, 255), (int(pos[0] + rad*np.cos(np.deg2rad(dir))), int(pos[1] - rad*np.sin(np.deg2rad(dir)))), (int(pos[0] + rad*np.cos(np.deg2rad(dir - 140))), int(pos[1] - rad*np.sin(np.deg2rad(dir - 140)))), 1)
            
        # Enemies
        for enemy in enemies:
            enemy.update(wn)
            if enemy.dead:
                engaged_with = None
                enemies.remove(enemy)

            if enemy.engaged:
                dir = enemy.get_dir()

            if enemy.pos[1] > sc_h - 70:
                hearts -= 1
                hurt_sound = mixer.Sound("Hurt.wav")
                hurt_sound.play()
                enemy.dead = True
                booms.append(Boom([enemy.pos[0], sc_h - 50]))
                boom_sound = mixer.Sound("Explosion.wav")
                boom_sound.play()

        # Enemy Spawning
        if len(enemies) < wave and not game_over:
            spawn_enemy(enemies, None)

        # Bullets
        for bullet in bullets:
            bullet.update(wn)
            if bullet.dead:
                bullets.remove(bullet)

        # Booms
        for boom in booms:
            boom.update(wn)
            if boom.dead:
                booms.remove(boom)

        # UI
        pygame.draw.rect(wn, (25, 25, 50), (0, 0, sc_w, 40))
        font = pygame.font.SysFont("Ariel", 30)
        if score <= 1000:
            text = font.render("Score " + str(int(score)), 1, (255, 255, 255))
        elif 1000 < score < 1000000:
            text = font.render("Score " + str(int(score/1000)) + "K", 1, (255, 255, 255))
        elif 10**6 <= score < 10**9:
            text = font.render("Score " + str(int(score/(10**6))) + "M", 1, (255, 255, 255))
        elif 10**9 <= score < 10**12:
            text = font.render("Score " + str(int(score/(10**9))) + "B", 1, (255, 255, 255))
        elif 10**12 <= score < 10**15:
            text = font.render("Score " + str(int(score/(10**12))) + "T", 1, (255, 255, 255))
        elif 10**15 <= score < 10**18:
            text = font.render("Score " + str(int(score/(10**15))) + "Q", 1, (255, 255, 255))
        else:
            text = font.render("Score Error", 1, (255, 255, 255))
        wn.blit(text, (sc_w - 120, 25 - text.get_height() / 2))
        if multiplier > 1:
            font = pygame.font.SysFont("Ariel", 25)
            text = font.render("x" + str(int(np.floor(multiplier))), 1, (255, 255, 255))
            wn.blit(text, (sc_w - 30, 25 - text.get_height() / 2))

        font = pygame.font.SysFont("Ariel", 30)
        text = font.render("Wave " + str(wave), 1, (200, 200, 200))
        wn.blit(text, (sc_w / 2 - text.get_width() / 2, 25 - text.get_height() / 2))
        
        # Hearts
        num = 0
        while 2 * num < hearts:
            pygame.draw.circle(wn, (255, 0, 80), (30 + num*30, 20), 10)
            num += 1

        if hearts == 0:
            game_over = True
            while len(enemies) > 1:
                for enemy in enemies:
                    enemies.remove(enemy)

        pygame.draw.line(wn, (255, 255, 255), (0, sc_h - 50), (sc_w, sc_h - 50), 5)

        # Game Over Screen
        if game_over:
            font = pygame.font.SysFont("Ariel", 60)
            text = font.render("Game Over Loser", 1, (255, 255, 255))
            wn.blit(text, (sc_w / 2 - text.get_width() / 2, 2*sc_h/7))
            buttons = [Button([sc_w / 3, 3*sc_h / 7], [sc_w / 4, 50], (30, 30, 30), (60, 60, 60), "Restart", (255, 255, 255), endless), 
                       Button([2*sc_w / 3, 3*sc_h / 7], [sc_w / 4, 50], (30, 30, 30), (60, 60, 60), "Menu", (255, 255, 255), menu)]
        for button in buttons:
            button.update(wn)

        pygame.display.update()

def lyrics_race(wn, file, mode):
    old_keys = pygame.key.get_pressed()
    mixer.music.load("Songs/" + file +".mp3")
    mixer.music.play()
    index = 0

    time_assist = 500

    transcript = []
    with open("Song_Lyrics/" + file + ".txt") as f:
        for line in f:
            transcript.append(line.strip())

    enemies = []
    bullets = []
    booms = []
    words = []
    buttons = []

    # Player Attributes
    rad = 20
    dir = 90
    pos = [int(sc_w / 2), int(8*sc_h / 9)]
    engaged_with = None
    paused = False
    game_over = False
    count = 0

    while True:
        wn.fill((0, 0, 0))
        clock.tick(60)

        # Clicking Actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    if button.highlighted:
                        button.func(wn)
        
        # Detect Keys
        if not game_over:
            old_keys, new_c, Enter, BackSpace = keyboard_detection(old_keys)
            if new_c != "":
                if engaged_with is None:
                    for enemy in enemies:
                        if enemy.word[0].lower() == new_c[0].lower():                   # Temporary lowercase only mode
                            enemy.engaged = True
                            engaged_with = enemy
                            if mode == "impossible" or mode == "hard":
                                for letter in new_c:
                                    engaged_with.attack(letter, bullets, booms)
                            elif mode == "easy" or mode == "medium":
                                engaged_with.attack(new_c[0], bullets, booms)
                                engaged_with.dead = True
                                break
                else:
                    for letter in new_c:
                        engaged_with.attack(letter, bullets, booms)

        # Music and Lyrics
        if index < len(transcript):
            if int(transcript[index]) <= mixer.music.get_pos() - time_assist:
                # Music Pausing
                if mode == "easy" or mode == "hard":
                    if index > 0 and len(enemies) > 0:
                        paused = True
                        mixer.music.pause()

                # Lyrics Spawning
                if not paused:
                    current_word = ""
                    for i in transcript[index + 1]:
                        if i == "(":
                            break
                        elif i != " ":
                            current_word += i
                        else:
                            words.append(current_word)
                            current_word = ""
                    if current_word != "":
                        words.append(current_word)
                    index += 2
        else:                                           # Check win
            if len(enemies) == 0:
                game_over = True
                buttons.append(Button([sc_w/2 + 100, sc_h/2 + 50], [200, 100], (30, 30, 30), (60, 60, 60), ("Menu"), (255, 255, 255), menu))

        if len(words) > 0 and count%20 == 0:
            spawn_enemy(enemies, words[0])
            words.remove(words[0])

        # Music Unpausing
        if paused and len(enemies) == 0:
            paused = False
            mixer.music.unpause()
            
        # Player
        pygame.draw.line(wn, (255, 255, 255), (pos[0], pos[1]), (int(pos[0] + rad*np.cos(np.deg2rad(dir + 140))), int(pos[1] - rad*np.sin(np.deg2rad(dir + 140)))), 1)
        pygame.draw.line(wn, (255, 255, 255), (pos[0], pos[1]), (int(pos[0] + rad*np.cos(np.deg2rad(dir - 140))), int(pos[1] - rad*np.sin(np.deg2rad(dir - 140)))), 1)
        pygame.draw.line(wn, (255, 255, 255), (int(pos[0] + rad*np.cos(np.deg2rad(dir))), int(pos[1] - rad*np.sin(np.deg2rad(dir)))), (int(pos[0] + rad*np.cos(np.deg2rad(dir + 140))), int(pos[1] - rad*np.sin(np.deg2rad(dir + 140)))), 1)
        pygame.draw.line(wn, (255, 255, 255), (int(pos[0] + rad*np.cos(np.deg2rad(dir))), int(pos[1] - rad*np.sin(np.deg2rad(dir)))), (int(pos[0] + rad*np.cos(np.deg2rad(dir - 140))), int(pos[1] - rad*np.sin(np.deg2rad(dir - 140)))), 1)
         
        # Enemies
        for enemy in enemies:
            enemy.update(wn)
            if enemy.dead:
                booms.append(Boom([enemy.pos[0], enemy.pos[1] + 24]))
                boom_sound = mixer.Sound("Explosion.wav")
                boom_sound.play()
                engaged_with = None
                enemies.remove(enemy)

            if enemy.engaged:
                dir = enemy.get_dir()

            if enemy.pos[1] > sc_h - 70:
                enemy.dead = True
                booms.append(Boom([enemy.pos[0], sc_h - 50]))
                boom_sound = mixer.Sound("Explosion.wav")
                boom_sound.play()

        # Bullets
        for bullet in bullets:
            bullet.update(wn)
            if bullet.dead:
                bullets.remove(bullet)

        # Booms
        for boom in booms:
            boom.update(wn)
            if boom.dead:
                booms.remove(boom)

        # Buttons
        for button in buttons:
            button.update(wn)

        # UI
        name = ""
        for i in file:
            if i != "_":
                name += i
            else:
                name += " "
        pygame.draw.rect(wn, (0, 0, 60), (0, 0, sc_w, 35))
        font = pygame.font.SysFont("Ariel", 30)
        title = font.render(name, 1, (255, 255, 255))
        wn.blit(title, (sc_w/2 - title.get_width() / 2, 20 - title.get_height() / 2))
        pygame.draw.line(wn, (255, 255, 255), (0, sc_h - 50), (sc_w, sc_h - 50), 5)

        if game_over:
            font = pygame.font.SysFont("Ariel", 50)
            text = font.render("You Win!", 1, (255, 255, 255))
            wn.blit(text, (sc_w / 2 - text.get_width()/2, sc_h / 2 - 100 - text.get_height()/2))

        count += 1
        pygame.display.update()

def song_menu(wn):
    # Song List
    songlist = []
    for path in os.listdir("Songs"):
        path = path[:-4]
        songlist.append(path)
    modes = ["Easy", "Medium", "Hard", "Impossible"]
    mode = "easy"

    buttons = [Button([90, 70], [80, 40], (30, 30, 30), (60, 60, 60), "Easy", (255, 255, 255), None),
               Button([190, 70], [80, 40], (30, 30, 30), (60, 60, 60), "Medium", (255, 255, 255), None),
               Button([290, 70], [80, 40], (30, 30, 30), (60, 60, 60), "Hard", (255, 255, 255), None),
               Button([390, 70], [80, 40], (30, 30, 30), (60, 60, 60), "Impossible", (255, 255, 255), None)]
    
    for song in songlist:
        title = ""
        for i in song:
            if i != "_":
                title += i
            else:
                title += " "
        buttons.append(Button([250, 200 + 100 * songlist.index(song)], [400, 80], (40, 40, 40), (60, 60, 60), title, (255, 255, 255), lyrics_race, var=song))
    while True:
        wn.fill((0, 0, 0))
        clock.tick(60)

        # Title
        font = pygame.font.SysFont("Ariel", 30)
        title = font.render("Choose Song to Play to", 1, (200, 200, 200))
        wn.blit(title, (sc_w/2 - title.get_width()/2, 10))

        # Song List
        for button in buttons:
            button.update(wn)

            if button.text.lower() == mode:
                button.col = (30, 70, 30)
                button.high_col = (60, 110, 60)
            else:
                button.col = (30, 30, 30)
                button.high_col = (60, 60, 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    if button.highlighted: 
                        if button.text not in modes:
                            if button.var is not None:
                                button.func(wn, button.var, mode)
                            else:
                                button.func(wn)
                        else:
                            mode = button.text.lower()

        pygame.display.update()

def callibrate(wn, file):
    old_keys = pygame.key.get_pressed()
    count = 0
    mixer.music.load("Songs/" + file + ".mp3")
    lyrics = []
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    with open("Song_Lyrics/" + file + ".txt") as f:
        for line in f:
            if line[0] not in numbers:
                lyrics.append(line.strip())
    mixer.music.play()
    index = 0
    time_stamps = []
    buttons = [Button([55, 25], [100, 40], (40, 40, 40), (60, 60, 60), "Main Menu", (255, 255, 255), menu)]
    while True:
        wn.fill((0, 0, 0))
        clock.tick(60)

        # Title
        title_font = pygame.font.SysFont("Ariel", 30)
        text = title_font.render("Callibration Mode", 1, (200, 200, 200))
        wn.blit(text, (sc_w / 2 - text.get_width()/2, 15))

        # Instructions
        font = pygame.font.SysFont("Ariel", 20)
        text = font.render("Press Space between the green and red lyrics", 1, (150, 150, 150))
        wn.blit(text, (sc_w/2 - text.get_width()/2, 45))
        text = font.render("End the song with Enter to save", 1, (150, 150, 150))
        wn.blit(text, (sc_w/2 - text.get_width()/2, 60))

        # Print Lyrics
        if index > 0:      
            size = 45
            font = pygame.font.SysFont("Ariel", size)
            line1 = font.render(lyrics[index - 1], 1, (255, 200, 200))
            while line1.get_width() > 9 *sc_w/10:
                size -= 1
                font = pygame.font.SysFont("Ariel", size)
                line1 = font.render(lyrics[index - 1], 1, (255, 170, 170))

        if index < len(lyrics):
            size = 45
            font = pygame.font.SysFont("Ariel", size)
            line2 = font.render(lyrics[index], 1, (170, 255, 170))
            while line2.get_width() > 9 *sc_w/10:
                size -= 1
                font = pygame.font.SysFont("Ariel", size)
                line2 = font.render(lyrics[index], 1, (200, 255, 200))

        if index > 0:
            wn.blit(line1, (sc_w / 2 - line1.get_width() / 2, sc_h / 2 - line1.get_height() / 2 - 30))
        if index < len(lyrics):
            wn.blit(line2, (sc_w / 2 - line2.get_width() / 2, sc_h / 2 - line2.get_height() / 2 + 30))

        # Swap Lyrics
        old_keys, new_c, Enter, BackSpace = keyboard_detection(old_keys)
        if new_c == " ":
            index += 1
            time_stamps.append(mixer.music.get_pos())
        if Enter:
            create_file(file, lyrics, time_stamps)
            menu(wn)

        # Clicking Actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    if button.highlighted:
                        button.func(wn)
        
        # buttons
        for button in buttons:
            button.update(wn)

        count += 1
        pygame.display.update()

def callibrate_menu(wn):
    # Song List
    songlist = []
    for path in os.listdir("Songs"):
        path = path[:-4]
        songlist.append(path)

    buttons = []
    for song in songlist:
        title = ""
        for i in song:
            if i != "_":
                title += i
            else:
                title += " "
        buttons.append(Button([250, 150 + 100 * songlist.index(song)], [400, 80], (40, 40, 40), (60, 60, 60), title, (255, 255, 255), callibrate, var=song))
    while True:
        wn.fill((0, 0, 0))
        clock.tick(60)

        # Title
        font = pygame.font.SysFont("Ariel", 30)
        title = font.render("Choose Song to Callibrate", 1, (200, 200, 200))
        wn.blit(title, (sc_w/2 - title.get_width()/2, 10))

        # Song List
        for button in buttons:
            button.update(wn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    if button.highlighted:
                        if button.var is not None:
                            button.func(wn, button.var)
                        else:
                            button.func(wn)

        pygame.display.update()

def create_file(file, lyrics, time_stamps):
    data = ""
    if len(time_stamps) != len(lyrics):
        print("Inequal")
    for index in range(len(time_stamps)):
            data += str(time_stamps[index]) + "\n"
            data += str(lyrics[index]) + "\n"
    with open("Song_Lyrics/" + file + ".txt", "w") as f:
        f.write(data)
    f.close()

def keyboard_detection(old_keys):
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    top_punctuation = ["!", "\"", "£", "$", "%", "^", "&", "*", "(", ")"]
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    new_character = ""
    Enter = False
    BackSpace = False

    keys = pygame.key.get_pressed()
    for index in range(0, len(keys)):
        if keys[index]:
            if not old_keys[index]:
                # Check numbers
                if not keys[304] and not keys[13]:
                    if 48 <= index <= 57:
                        new_character += numbers[index - 48]
                else:
                    if 48 <= index <= 57:
                        new_character += top_punctuation[index - 48]

                if 256 <= index <= 265:
                    new_character += numbers[index - 256]
                    
                
                # Check letters
                if 97 <= index <= 122:
                    if not keys[304] and not keys[13]:
                        new_character += letters[index - 97]
                    else:
                        new_character += letters[index - 97].upper()
                
                # Check functional characters
                if index == 13:
                    Enter = True
                elif index == 8:
                    BackSpace = True
                elif index == 32:
                    new_character += " "

                # Check punctuation
                if not keys[304] and not keys[13]:
                    if index == 44:
                        new_character += ","
                    elif index == 46:
                        new_character += "."
                    elif index == 47:
                        new_character += "/"
                    elif index == 92:
                        new_character += "\#"
                    elif index == 39:
                        new_character += "\'"
                    elif index == 59:
                        new_character += ";"
                    elif index == 45:
                        new_character += "-"
                    elif index == 61:
                        new_character += "="
                    elif index == 60:
                        new_character += "\\"
                    elif index == 91:
                        new_character += "["
                    elif index == 93:
                        new_character += "]"
                else:
                    if index == 44:
                        new_character += "<"
                    elif index == 46:
                        new_character += ">"
                    elif index == 47:
                        new_character += "?"
                    elif index == 92:
                        new_character += "~"
                    elif index == 39:
                        new_character += "@"
                    elif index == 59:
                        new_character += ":"
                    elif index == 45:
                        new_character += "_"
                    elif index == 61:
                        new_character += "+"
                    elif index == 60:
                        new_character += "|"
                    elif index == 91:
                        new_character += "{"
                    elif index == 93:
                        new_character += "}"

    return keys, new_character, Enter, BackSpace
            
def testing(wn):
    buttons = [Button([80, 45], [120, 50], [30, 30, 30], [60, 60, 60], "Main Menu", [200, 200, 200], menu)]
    old_keys = pygame.key.get_pressed()
    current_word = ""
    while True:
        wn.fill((0, 0, 0))
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    if button.highlighted:
                        select = mixer.Sound("ButtonSelect.wav")
                        select.play()
                        button.func(wn)

        # Main Event
        # Trying to make the most effective keyboard typing system
        old_keys, new_c, Enter, BackSpace = keyboard_detection(old_keys)

        # Testing New SetUp
        current_word += new_c
        if Enter:
            current_word = ""
        if BackSpace:
            current_word = current_word[:-1]

        font = pygame.font.SysFont("Ariel", 30)
        text = font.render(current_word, 1, (255, 255, 255))
        wn.blit(text, (sc_w/2 - text.get_width() / 2, sc_h/2 + 100 - text.get_height()/2))

        # Title
        font = pygame.font.SysFont("Ariel", 50)
        text = font.render("Keyboard Testing", 1, (255, 255, 255))
        wn.blit(text, (sc_w / 2 - text.get_width() / 2, 90))

        # Buttons
        for button in buttons:
            button.update(wn)

        pygame.display.update()

def spawn_enemy(enemies, word):
    if word is None:
        count = 0
        while word is None:
            count += 1
            word = random.choice(dictionary)
            for enemy in enemies:
                if word is not None:
                    if enemy.word[0] == word[0]:
                        word = None

            if count > 10:
                print("Unable to find word")
                break
    else:
        enemies.append(Enemy(word, 2))

def add_score(kill):
    global score, multiplier
    multipliers = [1, 2, 5, 10, 15, 25, 50, 75, 100]
    if kill:
        if multipliers.index(multiplier) < 8:
            multiplier = multipliers[multipliers.index(multiplier) + 1]
    score += 5 * np.floor(multiplier)

class Enemy(object):
    def __init__(self, word, speed):
        self.font = pygame.font.SysFont("ariel", 25, bold=False)
        x = sc_w/2
        while x == sc_w / 2:
            x = random.randrange(50, sc_w - 50)
        self.pos = [x, 0]
        self.word = word
        self.col = (255, 255, 255)
        self.fullhealth = len(self.word)
        if speed is None:
            self.speed = random.randint(1, 5)/3
        else:
            self.speed = speed
        self.engaged = False
        self.dead = False

    def update(self, wn):
        self.pos[1] += self.speed
        ratio = len(self.word) / self.fullhealth
        self.col = (255, 255*ratio, 255*(ratio**2))
        text = self.font.render(self.word, 1, self.col)
        wn.blit(text, (self.pos[0] - text.get_width() / 2, self.pos[1] - text.get_height() / 2))
        pygame.draw.circle(wn, (255, 255, 255), (int(self.pos[0]), int(self.pos[1] + 14)), 5)
        pygame.draw.circle(wn, (255, 255, 255), (int(self.pos[0]), int(self.pos[1] + 14)), 8, 1)

    def attack(self, letter, bullets, booms):
        global score, multiplier
        # Make Sound
        fire_sound = mixer.Sound("Fire.wav")
        fire_sound.play()
        if letter == self.word[0]:
            if len(self.word) > 1:
                pos, rad = [int(sc_w / 2), int(8*sc_h / 9)], 20
                dir = self.get_dir()
                bullets.append(Bullet((int(pos[0] + rad*np.cos(np.deg2rad(dir))), int(pos[1] - rad*np.sin(np.deg2rad(dir)))), (self.pos[0], self.pos[1] + 30)))
                self.word = self.word[1:]
                add_score(False)
            else: 
                pos, rad = [int(sc_w / 2), int(8*sc_h / 9)], 20
                dir = self.get_dir()
                bullets.append(Bullet([int(pos[0] + rad*np.cos(np.deg2rad(dir))), int(pos[1] - rad*np.sin(np.deg2rad(dir)))], [self.pos[0], self.pos[1] + 30]))
                self.dead = True
                add_score(True)
        else:
            pos, rad = [int(sc_w / 2), int(8*sc_h / 9)], 20
            dir = self.get_dir()
            bullets.append(Bullet((int(pos[0] + rad*np.cos(np.deg2rad(dir))), int(pos[1] - rad*np.sin(np.deg2rad(dir)))), (random.randint(0, sc_w), 0)))
            multiplier = 1
                          
    def get_dir(self):
        h = np.sqrt((self.pos[0] - sc_w/2) ** 2 + (self.pos[1] + 10 - 8*sc_h / 9)**2)
        a = self.pos[0] - sc_w / 2
        dir = np.arccos(a / h)
        return np.rad2deg(dir)
    
class Bullet(object):
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos
        if self.start_pos[0] != self.end_pos[0]:
            self.m = (self.start_pos[1] - self.end_pos[1]) / (self.start_pos[0] - self.end_pos[0])
        else:
            print("uhoh")
        self.count = random.randint(5, 20)
        self.len = random.randint(1, 3)
        self.dx = (self.end_pos[0] - self.start_pos[0])/self.count
        self.pos = [start_pos[0], start_pos[1]]
        self.pos1 = [start_pos[0], start_pos[1]]
        self.dead = False

    def update(self, wn):
        if self.start_pos[0] != self.end_pos[0]:
            self.pos[0] += self.dx
            self.pos[1] = self.m*(self.pos[0] - self.start_pos[0]) + self.start_pos[1]
            self.pos1[0] = self.pos[0] - self.len * self.dx
            self.pos1[1] = self.m*(self.pos1[0] - self.start_pos[0]) + self.start_pos[1]
            pygame.draw.line(wn, (255, 255, 0), (self.pos[0], self.pos[1]), (self.pos1[0], self.pos1[1]), 1)

            self.count -= 1

            if self.count < 0:
                self.dead = True

class Boom(object):
    def __init__(self, pos):
        self.pos = pos
        self.count = random.randint(14, 25)
        self.size = self.count
        self.dead = False
        self.col = random.choice([[200, 100, 0], [255, 200, 0], [255, 100, 0], [150, 150, 0], [230, 150, 0], [255, 255, 0], [230, 130, 0], [240, 120, 0]])

    def update(self, wn):
        pygame.draw.circle(wn, self.col, (int(self.pos[0]), int(self.pos[1])), self.size - self.count)
        pygame.draw.circle(wn, (255, 255, 255), (int(self.pos[0]), int(self.pos[1])), int((self.size - self.count) / 2))
        self.count -= 1

        if self.count == 0:
            self.dead = True

class Button(object):
    def __init__(self, pos, dim, col, high_col, text, text_col, func, var=None):
        self.pos = pos
        self.dim = dim
        self.col = col
        self.high_col = high_col
        self.text = text
        self.text_col = text_col
        self.highlighted = False
        self.func = func
        self.var = var

        # Adjust text
        if self.text is not None:
            size = 1
            font = pygame.font.SysFont("Ariel", size)
            self.ftext = font.render(self.text, 1, self.text_col)
            while self.ftext.get_width() < 4 * self.dim[0] /5:
                size += 1
                font = pygame.font.SysFont("Ariel", size)
                self.ftext = font.render(self.text, 1, self.text_col)

    def update(self, wn):
        pos = pygame.mouse.get_pos()
        if (self.pos[0] - self.dim[0] / 2 < pos[0] < self.pos[0] + self.dim[0] / 2) and (self.pos[1] - self.dim[1] / 2 < pos[1] < self.pos[1] + self.dim[1] / 2):
                pygame.draw.rect(wn, self.high_col, (self.pos[0] - self.dim[0] / 2, self.pos[1] - self.dim[1] / 2, self.dim[0], self.dim[1]))
                self.highlighted = True
        else:
            pygame.draw.rect(wn, self.col, (self.pos[0] - self.dim[0] / 2, self.pos[1] - self.dim[1] / 2, self.dim[0], self.dim[1]))
            self.highlighted = False
        wn.blit(self.ftext, (self.pos[0] - self.ftext.get_width() / 2, self.pos[1] - self.ftext.get_height() / 2))

if __name__ == "__main__":
    menu(wn)