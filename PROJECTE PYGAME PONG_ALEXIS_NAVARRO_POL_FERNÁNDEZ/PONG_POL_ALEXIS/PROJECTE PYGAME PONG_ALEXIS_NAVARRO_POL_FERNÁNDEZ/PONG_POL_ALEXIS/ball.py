import pygame
from random import randint
GREEN = (0, 143, 57);

class Pilota(pygame.sprite.Sprite):
    #La classe representa la pilota i deriva de la classe Sprite de Pygame
    def __init__(self, color, width, height):
        # Crida al constructor de la classe mare (Sprite)
        super().__init__()
        
        # Li passem el color de la pilota
        # Posem color VERD fons per ser INDEPENDENT/transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
        self.image.set_colorkey(GREEN)

        # Dibuixa la pilota (un rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        self.velocity = [randint(4,8),randint(-8,8)] #[vel.x, vel.y]
        
        # Busca el obj rectangle amb les dimensions de la imatge
        self.rect = self.image.get_rect()
        
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8,8)

