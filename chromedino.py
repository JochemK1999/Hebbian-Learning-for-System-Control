# !/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import os
import random
import threading
import csv

import pygame

from HebbianNetwork import HebbianNetwork

pygame.init()

# Global Constants

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

NETWORK_PLAY = True

pygame.display.set_caption("Chrome Dino Runner")

Ico = pygame.image.load("assets/DinoWallpaper.png")
pygame.display.set_icon(Ico)

RUNNING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoRun2.png")),
]
JUMPING = pygame.image.load(os.path.join("assets/Dino", "DinoJump.png"))

DUCKING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck2.png")),
]

SMALL_CACTUS = [
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus3.png")),
]

LARGE_CACTUS = [
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus3.png")),
]

BIRD = [
    pygame.image.load(os.path.join("assets/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("assets/Bird", "Bird2.png")),
]

CLOUD = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("assets/Other", "Track.png"))

FONT_COLOR=(0,0,0)

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 17
    GRAVITY = 1

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.jump_holddown = 0

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.gravity = self.GRAVITY
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_bounding_rect().inflate(-10, 0)
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 20:
            self.step_index = 0

        if userInput == "jump" and not self.dino_jump:
            self.jump_holddown = 0
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput == "jump" and self.dino_jump:
            self.jump_holddown += 1
            if self.jump_holddown > 10:
                self.gravity = 0.5
        elif userInput == "duck" and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput == "duck"):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
        
    def duck(self):
        self.image = self.duck_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect().inflate(-10, 0)
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel
            self.jump_vel -= self.gravity
        if self.dino_rect.y >= self.Y_POS:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
            self.gravity = self.GRAVITY

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop(0)

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    BIRD_HEIGHTS = [220, 270, 320]

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 19:
            self.index = 0
        SCREEN.blit(self.image[self.index // 10], self.rect)
        self.index += 1

class DataRecorder():
    def __init__(self, measuring_places):
        self.inputs = []
        self.outputs = []
        self.headers = measuring_places.copy()
        self.headers.append("output")
    
    def record(self, inputs, output):
        self.inputs.append(inputs)

        if (output[pygame.K_UP] or output[pygame.K_SPACE]):
            self.outputs.append("jump")
        elif output[pygame.K_DOWN]:
            self.outputs.append("duck")
        else:
            self.outputs.append("nothing")

    def remove_death(self):
        removed_datapoints = 0
        """
        while(sum(self.inputs[-1]) > 0):
            self.inputs.pop()
            self.outputs.pop()
            removed_datapoints += 1
        """

        self.inputs = self.inputs[:-50]
        self.outputs = self.outputs[:-50]
        removed_datapoints = 50

        print(f"Removed {removed_datapoints} datapoints")

    def save(self, filename):        
        file_exists = os.path.isfile(filename)

        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(self.headers)  # Add header if the file is newly created
            
            for i, j in zip(self.inputs, self.outputs):
                writer.writerow(i + [j])

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []
    death_count = 0
    pause = False
    next_distance = random.randint(0, 400)
    measuring_places = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800]
    recorder = DataRecorder(measuring_places)
    
    if NETWORK_PLAY:
        network = HebbianNetwork.from_file('network.npy')

    def score():
        global points, game_speed
        points += 1
        
        #Speed up the game
        #if points % 100 == 0:
        #    game_speed += 1
        
        text = font.render("Points: " + str(points), True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)
    
    def detector():
        detections = []
        for i in measuring_places:
            detections.append(0)
            for j in obstacles:
                if j.rect.x < i < j.rect.x + j.rect.width:
                    if type(j) == Bird:
                        if j.rect.y == j.BIRD_HEIGHTS[0]:
                            detections[-1] = 3
                        elif j.rect.y == j.BIRD_HEIGHTS[1]:
                            detections[-1] = 2
                        else:
                            detections[-1] = 1
                    else:
                        detections[-1] = 1
                    break
        
        return detections   
    
    def draw_detectors():
        for i, j in zip(measuring_places, detector()):
            pygame.draw.line(SCREEN, (0 if j else 255, 255 if j else 0, 0), (i, 0), (i, 390), 1)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def unpause():
        nonlocal pause, run
        pause = False
        run = True

    def paused():
        nonlocal pause
        pause = True
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("Game Paused, Press 'u' to Unpause", True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT  // 3)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    unpause()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                run = False
                paused()

        # Add a new obstacle
        #print(obstacles[-1].rect.x if obstacles else 0)
        if len(obstacles) == 0 or (obstacles[-1].rect.x < 700 and 700 - obstacles[-1].rect.x > next_distance):
            next_distance = random.randint(0, 400)
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        if NETWORK_PLAY:
            botInput = network.predict(detector())
            player.update(botInput)
        else:
            userInput = pygame.key.get_pressed()

            if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]):
                player.update("jump")
            elif userInput[pygame.K_DOWN]:
                player.update("duck")
            else:
                player.update("nothing")

            recorder.record(detector(), userInput)
        
        SCREEN.fill((255, 255, 255))
        background()
        score()
        player.draw(SCREEN)
        draw_detectors()

        # Draw the obstacle
        for obstacle in reversed(obstacles):
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.display.update()
                if not NETWORK_PLAY:
                    recorder.remove_death()
                    recorder.save("data.csv")

                pygame.time.delay(500)
                death_count += 1
                menu(death_count)

        

        clock.tick(60)
        pygame.display.update()


def menu(death_count):
    global points
    global FONT_COLOR
    run = True
    while run:        
        FONT_COLOR=(0,0,0)
        SCREEN.fill((255, 255, 255))
        
        font = pygame.font.Font("freesansbold.ttf", 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, FONT_COLOR)
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, FONT_COLOR)
            score = font.render("Your Score: " + str(points), True, FONT_COLOR)
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()


t1 = threading.Thread(target=menu(death_count=0), daemon=True)
t1.start()
