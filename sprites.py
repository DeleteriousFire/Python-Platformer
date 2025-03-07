import pygame
from os import listdir
from os.path import isfile, join

pygame.init()
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