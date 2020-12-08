import pygame

GREEN = (0, 143, 57);

class Jugador(pygame.sprite.Sprite):
    #La classe representa un jugador i deriva de la classe Sprite de Pygame
    
    def __init__(self, color, width, height):
        # Crida al constructor de la classe mare (Sprite)
        super().__init__()
        
        # Li passem el color del jugador, la posició X,Y i width i height
        # Posem color VERD fons per ser INDEPENDENT/transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
        self.image.set_colorkey(GREEN)

        # Dibuixar al jugador (un rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        # Busca el obj rectangle amb les dimensions de la imatge
        self.rect = self.image.get_rect()

#Moviments jugadors
    def moveUp(self, pixels):
        self.rect.y -= pixels
		#Evita sortir fora de la finestra!
        if self.rect.y < 0:
            self.rect.y = 0
        
    def moveDown(self, pixels):
        self.rect.y += pixels
	    #Evita sortir fora de la finestra!
        if self.rect.y > 500:
            self.rect.y = 500