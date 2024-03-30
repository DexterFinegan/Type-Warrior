# A game where enemies are words of varying length and you fight them by typing out the word
# 3-4-23

import pygame
from pygame import mixer
import random
import numpy as np

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
    buttons = [Button([sc_w / 2, 3*sc_h / 5], [sc_w/2, 80], [30, 30, 30], [60, 60, 60], "Endless", [200, 200, 200], main)]
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
        version = font.render("Version 1", 1, (100, 100, 100))
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

def main(wn):
    global score, multiplier
    old_keys = pygame.key.get_pressed()
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    enemies = []
    bullets = []
    booms = []
    current_word = ""
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
        keys = pygame.key.get_pressed()
        if not game_over:
            for key in keys:
                if key and not old_keys[keys.index(key)]:
                    if 97 <= keys.index(key) <= 123:                # Keeps to just letter characters
                        current_word = current_word + letters[keys.index(key) - 97]

                        if engaged_with is None:
                            for enemy in enemies:
                                if enemy.word[0] == letters[keys.index(key) - 97]:
                                    enemy.engaged = True
                                    engaged_with = enemy
                                    engaged_with.attack(letters[keys.index(key) - 97], bullets, booms)
                        else:
                            engaged_with.attack(letters[keys.index(key) - 97], bullets, booms)

                    elif keys.index(key) == 13:
                        current_word = ""
                    elif keys.index(key) == 9:
                        spawn_enemy(enemies)
                    else:
                        print(keys.index(key))
        old_keys = keys

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
                current_word = ""

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
            spawn_enemy(enemies)

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
            buttons = [Button([sc_w / 3, 3*sc_h / 7], [sc_w / 4, 50], (30, 30, 30), (60, 60, 60), "Restart", (255, 255, 255), main), 
                       Button([2*sc_w / 3, 3*sc_h / 7], [sc_w / 4, 50], (30, 30, 30), (60, 60, 60), "Menu", (255, 255, 255), menu)]
        for button in buttons:
            button.update(wn)

        pygame.display.update()

def spawn_enemy(enemies):
    word = None
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
    
    if word is not None:
        enemies.append(Enemy(word))

def add_score(kill):
    global score, multiplier
    multipliers = [1, 2, 5, 10, 15, 25, 50, 75, 100]
    if kill:
        if multipliers.index(multiplier) < 8:
            multiplier = multipliers[multipliers.index(multiplier) + 1]
    score += 5 * np.floor(multiplier)

class Enemy(object):
    def __init__(self, word):
        self.font = pygame.font.SysFont("ariel", 25, bold=False)
        x = sc_w/2
        while x == sc_w / 2:
            x = random.randrange(50, sc_w - 50)
        self.pos = [x, -100]
        self.word = word
        self.col = (255, 255, 255)
        self.fullhealth = len(self.word)
        self.speed = random.randint(1, 5)/3
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
                booms.append(Boom([self.pos[0], self.pos[1] + 24]))
                boom_sound = mixer.Sound("Explosion.wav")
                boom_sound.play()
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
    def __init__(self, pos, dim, col, high_col, text, text_col, func):
        self.pos = pos
        self.dim = dim
        self.col = col
        self.high_col = high_col
        self.text = text
        self.text_col = text_col
        self.highlighted = False
        self.func = func

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