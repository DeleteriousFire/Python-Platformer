import pygame, random, sys, math
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("Platformer")

#CONSTANT VARIABLES
WIDTH, HEIGHT = 958, 800
PLAYER_VEL = 5
FPS = 60


screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
dt = 0

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheet(dir1, dir2, width, height, direction = False):
    path = join('Platformer/Python-Platformer/assets', dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(".png")]
    all_sprites = {}
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
    
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0,0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace('.png', '') + '_right'] = sprites
            all_sprites[image.replace('.png', '') + '_left'] = flip(sprites)
        else:
            all_sprites[image.replace('.png', '')] = sprites
    return all_sprites

def load_block(size):
    path = join('Platformer/Python-Platformer/assets', 'Terrain', 'Terrain.png')
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 128, size, size)
    surface.blit(image, (0,0), rect)
    return pygame.transform.scale2x(surface)


def get_background(name):
    image = pygame.image.load(join("Platformer", "Python-Platformer/assets/Background", name))
    _, _, width_tile, height_tile = image.get_rect()
    tiles = []

    for i in range(WIDTH//width_tile + 1):
        for j in range(HEIGHT//height_tile + 1):
            pos =(i * width_tile, j * height_tile)
            tiles.append(pos)
    return tiles, image

class Player(pygame.sprite.Sprite):
    GRAVITY = 0.5
    ANIMATION_DELAY = 4
    SPRITES = load_sprite_sheet("MainCharacters", "MaskDude", 32, 32, True)

    def __init__(self, x , y, width_player, height_player):
        super().__init__()
        self.rect = pygame.Rect(x, y, width_player, height_player)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.fall_duration = 0
        self.animation_counter = 0

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

    def landed(self):
        self.fall_duration = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel = -1

    def loop(self, fps):
        self.y_vel += min(5, (self.fall_duration / fps)* self.GRAVITY)
        self.move(self.x_vel, self.y_vel) 
        self.fall_duration += 1

        self.update_sprite()
        self.update()
       
    def update_sprite(self):
        sprite_sheet = 'idle'
        if self.x_vel > 0 or self.x_vel < 0:
            sprite_sheet = 'run'
        if self.y_vel < 0:
            sprite_sheet = 'jump'
        
        sprite_sheet_name = sprite_sheet + '_' + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = self.animation_counter // self.ANIMATION_DELAY % len(sprites)

        self.sprite = sprites[sprite_index]
        self.animation_counter += 1

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))  

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = load_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

def draw(screen, background, bg_image, player, objects):
    for tile in background:
        screen.blit(bg_image, tuple(tile))
    player.draw(screen)

    for obj in objects:
        obj.draw(screen)
    pygame.display.update()


def handle_vert_collision(player, objects, dy):
    collided_objects = []

    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
        collided_objects.append(obj)

    return collided_objects

def handle_movement(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)

    handle_vert_collision(player, objects, player.y_vel)

def main(screen):
    running = True
    player = Player(100, 100, 50, 50)
    block_size = 96
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) 
             for i in range(-WIDTH // 2, (WIDTH * 2) // block_size)]

    while running:
        background, bg_image = get_background("Pink.png")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                sys.exit()
            

       
        player.loop(FPS)

        handle_movement(player, floor)

        draw(screen, background, bg_image, player, floor)
        pygame.display.flip()

        dt = clock.tick(FPS)



if __name__ == "__main__":
    main(screen)