import pygame
from sys import exit # to end code whenever you call it
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('Pygame/UltimatePygameIntro/graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('Pygame/UltimatePygameIntro/graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('Pygame/UltimatePygameIntro/graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('Pygame/UltimatePygameIntro/audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('Pygame/UltimatePygameIntro/graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('Pygame/UltimatePygameIntro/graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        elif type == 'snail':
            snail_1 = pygame.image.load('Pygame/UltimatePygameIntro/graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('Pygame/UltimatePygameIntro/graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

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
    game_name_rect = game_name.get_rect(center = (400, 80))

    
    game_message = test_font.render("Press space to run", False, (111, 196, 169))
    game_message_rect = game_message.get_rect(center = (400, 320))

    screen.blit(game_name, game_name_rect)
    screen.blit(game_message, game_message_rect)

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    current_time /= 1000 # get second
    current_time = int(current_time)
    score_surf = test_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
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
# fps: frames/second
fps = 60
screen = pygame.display.set_mode((800, 400))
sky_surface = pygame.image.load('Pygame/UltimatePygameIntro/graphics/Sky.png').convert()
ground_surface = pygame.image.load('Pygame/UltimatePygameIntro/graphics/ground.png').convert()
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('Pygame/UltimatePygameIntro/font/Pixeltype.ttf', 50)
game_active = False 
start_time = 0
score = 0

bg_music = pygame.mixer.Sound('Pygame/UltimatePygameIntro/audio/music.wav')
bg_music.set_volume(0.2)
bg_music.play(loops = 6)

# Obstacle

# Snail
snail_frame_1 = pygame.image.load('Pygame/UltimatePygameIntro/graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('Pygame/UltimatePygameIntro/graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_frame_1 = pygame.image.load('Pygame/UltimatePygameIntro/graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('Pygame/UltimatePygameIntro/graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

# Player
player_walk_1 = pygame.image.load('Pygame/UltimatePygameIntro/graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('Pygame/UltimatePygameIntro/graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('Pygame/UltimatePygameIntro/graphics/Player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Intro screen
player_stand = pygame.image.load('Pygame/UltimatePygameIntro/graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

# Timer
obstacle_timer = pygame.USEREVENT + 1 # some events are already reserved in pygame
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
        else: 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, sky_surface.get_height()))
        score = display_score()

        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()

        # colllision: game over
        game_active = collision_sprite()
        
    else: 
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        score_message = test_font.render(f"Your score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 330))

        if score == 0:
            start_game()
        else: 
            screen.blit(score_message, score_message_rect)

    pygame.display.update()

    # the while loop shouldn't run faster than fps frames/second
    clock.tick(fps) 