import pygame


class Sprite:
    def __init__(self):
        self.sprites = {}
        self.path = "images/"

    def get_sprite(self, name, flipped=False):
        if (name, flipped) not in self.sprites.keys():
            path = self.path + name + ".png"
            image = pygame.image.load(path).convert_alpha()
            image = image if not flipped else pygame.transform.flip(image, True, False)
            self.sprites[(name, flipped)] = image
        return self.sprites[(name, flipped)]


sprite = Sprite()
