import pygame
from main import load_sprite_sheet


class Player(pygame.sprite.Sprite):
    GRAVITY = 0.5
    SPRITES = load_sprite_sheet("MainCharacters", "MaskDude", 32, 32, True)
    def __init__(self, x , y, width_player, height_player):
        self.rect = pygame.Rect(x, y, width_player, height_player)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.fall_duration = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_counter = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_counter = 0

    def loop(self, fps):
        self.y_vel += min(5, (self.fall_duration / fps)* self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        self.fall_duration += 1
        
    
    def draw(self, screen):
        self.sprite = self.SPRITES['idle_' + self.direction][0]
        screen.blit(self.sprite, (self.rect.x, self.rect.y))
