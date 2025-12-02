import pygame
import math
import random
import time

pygame.init()

WIDTH, HEIGHT = 1366, 768

TITLE_WIDTH, TITLE_HEIGHT = 1536 / 2, 547 / 2

OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 1054, 283 / 4

PLAYER_WIDTH, PLAYER_HEIGHT = 566 / 5, 681 / 5

DEATH_SCREEN = pygame.transform.scale(pygame.image.load('death_screen.png'), (WIDTH, HEIGHT))
DEATH_SCREEN_WIDTH, DEATH_SCREEN_HEIGHT = 500,500

START_BUTTON_WIDTH, START_BUTTON_HEIGHT = 1706, 130

OBSTACLE_OFFSET = 250

#Values for background scrolling effect
background1_y = 0
background2_y = -HEIGHT
background_vel = 1

FONT = pygame.font.Font('Sprintura.otf', 50)
SCORE_TEXT = FONT.render('SCORE:', True, (255,255,255))
HIGH_SCORE_TEXT = FONT.render('High Score:', True, (255,255,255))

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Derivative Dodge')

background = pygame.transform.scale(pygame.image.load('game_background.png').convert_alpha(), (WIDTH, HEIGHT))

def draw_before_title(background, sine_sprites, high_score_value, high_score_text):
    window.blit(background, (0,0))
    window.blit(high_score_value, (430,0))
    window.blit(high_score_text, (0,0))
    sine_sprites.draw(window)

    pygame.display.flip()
    pygame.display.update()

def draw_after_title(background, player, obstacle_left, obstacle_right, score_text, score_value):
    window.blit(background, (0,background1_y))
    window.blit(background, (0,background2_y))
    window.blit(player.image, player.rect)
    window.blit(obstacle_left.image, obstacle_left.rect)
    window.blit(obstacle_right.image, obstacle_right.rect)
    window.blit(score_text, (0,0))
    window.blit(score_value, (255,0))

    pygame.display.update()

def main():

    global background1_y, background2_y, background_vel

    #Sprite Velocities
    OBSTACLE_VEL = 4

    #Creating Sprites
    class PLAYER(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load('e.png').convert_alpha(), (PLAYER_WIDTH, PLAYER_HEIGHT))
            self.rect = self.image.get_rect()
            self.rect.x = WIDTH / 2 - PLAYER_WIDTH / 2
            self.rect.y = 600
            self.rect = pygame.Rect(self.rect.x,self.rect.y,100,100)

    class TITLE(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load('derivative_dodge_title_sprite.png').convert_alpha(), (TITLE_WIDTH , TITLE_HEIGHT))
            self.rect = self.image.get_rect()
            self.rect.x = WIDTH / 2 - TITLE_WIDTH / 2
            self.angle = 0

        def update(self):
            self.angle += 0.1
            self.rect.y = 100 + 5 * math.sin(self.angle)
            self.rect.x = (WIDTH / 2 - TITLE_WIDTH / 2) + 5 * math.cos(self.angle)

    class OBSTACLE_RIGHT(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load('vector_obstacle_right.png').convert_alpha(), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
            self.rect = self.image.get_rect()
            self.center_x = -550
            self.rect.y = -491
            self.rect = pygame.Rect(self.rect.x,self.rect.y,1024,50)
            self.angle = 0
        def reset(self):
            self.center_x = random.randint(-OBSTACLE_WIDTH + 200, -50)
            self.rect.y = -100
        def update_obst(self):
            self.rect.y += OBSTACLE_VEL
            self.angle += 0.1
            self.rect.x = self.center_x + 10 * math.sin(self.angle)
            if self.rect.y > HEIGHT:
                self.reset()
    
    class OBSTACLE_LEFT(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load('vector_obstacle_left.png').convert_alpha(), (OBSTACLE_WIDTH , OBSTACLE_HEIGHT))
            self.rect = self.image.get_rect()
            self.center_x = 750
            self.rect.y = -500
            self.rect = pygame.Rect(self.rect.x,self.rect.y,1024,50)
            self.angle = 0
        def reset(self):
            self.center_x = obstacle_right.center_x + OBSTACLE_OFFSET + OBSTACLE_WIDTH
            self.rect.y = -100
        def update_obst(self):
            self.rect.y += OBSTACLE_VEL
            self.angle += 0.1
            self.rect.x = self.center_x + 10 * math.cos(self.angle + 0.5 * math.pi)
            if self.rect.y > HEIGHT:
                self.reset()


    class START_BUTTON(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load('press-space-to-start.png').convert_alpha(), (START_BUTTON_WIDTH / 4, START_BUTTON_HEIGHT / 4))
            self.rect = self.image.get_rect()
            self.rect.x = (WIDTH / 2) - ((START_BUTTON_WIDTH / 4) / 2)
            self.x_value = 0

        def update(self):
            self.x_value += 0.1
            self.rect.y = 625 + 5 * math.sin(self.x_value)

    #Game status variables
    running = True
    in_game = False
    dead = True
   
    #Naming Sprites  
    player = PLAYER()
    obstacle_left = OBSTACLE_LEFT()
    obstacle_right = OBSTACLE_RIGHT()   
    start_button = START_BUTTON()
    title = TITLE()
    sine_sprites = pygame.sprite.Group(title, start_button)
    
    #Score Variables
    score_text = SCORE_TEXT
    score = 0
    high_score = 0
    high_score_text = HIGH_SCORE_TEXT


    clock = pygame.time.Clock()

    while running:
        clock.tick(60)

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    in_game = True
                    score = 0
                    dead = False
                    start_time = time.time()
                break
        
        if dead:
            obstacle_right.rect.y = -491
            obstacle_left.rect.y = -500

        if in_game:
            elapsed_time = time.time() - start_time
            OBSTACLE_VEL = 4 +int((elapsed_time // 10))
            PLAYER_VEL = 6 +int((elapsed_time // 10))
        obstacle_right.update_obst()
        obstacle_left.update_obst()
        sine_sprites.update()
        
        #Scrolling Background
        background1_y += background_vel
        background2_y += background_vel
        if background1_y >= HEIGHT:
            background1_y = -HEIGHT
        if background2_y >= HEIGHT:
            background2_y = -HEIGHT

        if in_game:
            if keys[pygame.K_a] and player.rect.x > 0 and in_game == True:
                player.rect.x -= PLAYER_VEL
            if keys[pygame.K_d] and player.rect.x + PLAYER_WIDTH < WIDTH and in_game == True:
                player.rect.x += PLAYER_VEL
            if keys[pygame.K_ESCAPE]:
                running = False

        #Collisions
        if not dead:
            prev_line_y = obstacle_left.rect.y - OBSTACLE_VEL
            curr_line_y = obstacle_left.rect.y
            if player.rect.colliderect(obstacle_left.rect) or player.rect.colliderect(obstacle_right.rect):
                transparent_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                transparent_surface.fill((255, 0, 0, 60))
                window.blit(DEATH_SCREEN, (0,0))
                window.blit(transparent_surface, (0,0))
                pygame.display.update()
                time.sleep(3)
                in_game = False
                dead = True
            if prev_line_y < player.rect.y <= curr_line_y:
                score += 1
        SCORE = FONT.render(str(score), True, (255,255,255))
        score_value = SCORE
        if score > high_score:
            high_score = score
        HIGH_SCORE = FONT.render(str(high_score), True, (255,255,255))
        high_score_value = HIGH_SCORE

        if not in_game:
            player.rect.x = WIDTH / 2 - PLAYER_WIDTH / 2
            player.rect.y = 600
        if in_game == True:
            draw_after_title(background, player, obstacle_left, obstacle_right, score_text, score_value)
        if in_game == False:
            draw_before_title(background, sine_sprites, high_score_value, high_score_text)
    pygame.quit()
main()