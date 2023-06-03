import pygame
from sys import exit # to end code whenever you call it
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('main/resources/graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('main/resources/graphics/Player/player_walk_2.png').convert_alpha()

        first_char_w = player_walk_1.get_width()
        first_char_h = player_walk_1.get_height()

        self.h_ratio = screen.get_height()/400
        self.w_ratio = screen.get_width()/800

        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('main/resources/graphics/Player/jump.png').convert_alpha()
        # self.player_shrink = pygame.image.load('main/resources/graphics/Player/shrink.png').convert_alpha()
        self.player_shrink = pygame.transform.rotozoom(self.player_jump, 0, 0.5)

        self.image = self.player_walk[self.player_index]
        self.image = pygame.transform.scale_by(self.image, (self.w_ratio, self.h_ratio))
        self.player_first_x = screen.get_width()/10
        self.player_first_y = screen.get_height() - ground_surface.get_height() # player first spawn on the ground
        self.rect = self.image.get_rect(midbottom = (self.player_first_x, self.player_first_y))
        self.gravity = 0
        self.isShrink = False

        self.jump_sound = pygame.mixer.Sound('main/resources/audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= (screen.get_height() - ground_surface.get_height()):
            self.gravity = -20
            self.jump_sound.play()
        elif keys[pygame.K_LSHIFT] and self.rect.bottom >= (screen.get_height() - ground_surface.get_height()):
            self.isShrink = True
            print('shrink')

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= (screen.get_height() - ground_surface.get_height()):
            self.rect.bottom = screen.get_height() - ground_surface.get_height()

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

    def animation_state(self):
        self.h_ratio = screen.get_height()/400
        self.w_ratio = screen.get_width()/800

        if self.rect.bottom < screen.get_height()/4*3:
            self.image = self.player_jump
            self.image = pygame.transform.scale_by(self.image, (self.w_ratio, self.h_ratio))
        else:
            if self.isShrink == True:
                # self.image = self.player_shrink = pygame.transform.scale(self.player_shrink, (self.player_shrink.get_width(), self.player_shrink.get_height()))
                self.image = self.player_shrink
                self.image = pygame.transform.scale_by(self.image, (self.w_ratio, self.h_ratio))
                self.isShrink = False
                self.player_first_x = screen.get_width()/10
                self.player_first_y = screen.get_height()/4*3
                self.rect = self.image.get_rect(midbottom = (self.player_first_x, self.player_first_y))
            else:
                self.player_index += 0.1
                if self.player_index >= len(self.player_walk):
                    self.player_index = 0
                self.image = self.player_walk[int(self.player_index)]
                self.image = pygame.transform.scale_by(self.image, (self.w_ratio, self.h_ratio))
                self.player_first_x = screen.get_width()/10
                self.player_first_y = screen.get_height()/4*3
                self.rect = self.image.get_rect(midbottom = (self.player_first_x, self.player_first_y))
        # print(f"{self.rect.bottom} {self.rect.top} {self.rect.right} {self.rect.left}")

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('main/resources/graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('main/resources/graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = screen.get_height()/5
        elif type == 'snail':
            snail_1 = pygame.image.load('main/resources/graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('main/resources/graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = screen.get_height() - ground_surface.get_height()

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def start_game():
    game_name = test_font.render("Pixel Jumper", False, (111, 196, 169))
    game_name_rect = game_name.get_rect(center = (screen.get_width()/2, screen.get_height()/5))

    
    game_message = test_font.render("Press space to run", False, (111, 196, 169))
    game_message_rect = game_message.get_rect(center = (screen.get_width()/2, screen.get_height()/5 * 4))

    screen.blit(game_name, game_name_rect)
    screen.blit(game_message, game_message_rect)

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    current_time /= 1000 # get second
    current_time = int(current_time)
    score_surf = test_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (screen.get_width()/2, screen.get_height()/5))
    screen.blit(score_surf, score_rect)
    return current_time

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    return True

pygame.init()
fps = 60
screen = pygame.display.set_mode((800, 400), pygame.RESIZABLE)
sky_surface = pygame.image.load('main/resources/graphics/Sky.png').convert()
ground_surface = pygame.image.load('main/resources/graphics/ground.png').convert()
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('main/resources/font/Pixeltype.ttf', 50)
game_active = False 
start_time = 0
score = 0

bg_music = pygame.mixer.Sound('main/resources/audio/music.wav')
bg_music.set_volume(0.2)
bg_music.play(loops = 6)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Intro screen
player_stand = pygame.image.load('main/resources/graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
# player_stand_rect = player_stand.get_rect(center = (400, 200))

# Timer
obstacle_timer = pygame.USEREVENT + 1 # some events are already reserved in pygame
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
        else: 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:
        # screen.blit(sky_surface, (0, 0))
        # sky_rect = sky_surface.get_rect(center = (screen.get_width()/2, screen.get_height()/2))
        # screen.blit(sky_surface, sky_rect)
        sky_surface = pygame.transform.scale(sky_surface, (screen.get_width(), screen.get_height()))
        screen.blit(sky_surface, (0, 0))

        ground_surface = pygame.transform.scale(ground_surface, (screen.get_width(), screen.get_height()/4))
        screen.blit(ground_surface, (0, sky_surface.get_height()/4*3))
        score = display_score()

        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()

        # colllision: game over
        game_active = collision_sprite()
        
    else: 
        screen.fill((94, 129, 162))
        player_stand_rect = player_stand.get_rect(center = (screen.get_width()/2, screen.get_height()/2))
        screen.blit(player_stand, player_stand_rect)
        player_gravity = 0

        score_message = test_font.render(f"Your score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (screen.get_width()/2, screen.get_height()/5*4))

        if score == 0:
            start_game()
        else: 
            screen.blit(score_message, score_message_rect)

    pygame.display.update()

    # the while loop shouldn't run faster than fps frames/second
    clock.tick(fps) 