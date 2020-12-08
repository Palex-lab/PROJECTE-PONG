#MAIN
import pygame, time, sys, cv2 #opencv-python
from random import randint 
from jugador import Jugador
from ball import Pilota
from ffpyplayer.player import MediaPlayer

pygame.init()

#Definim Colors
BLACK = (0, 0, 0);
WHITE = (255, 255, 255);
GREEN = (0, 143, 57);
FPS = 60

# Imatges del joc
campnou = pygame.image.load("camp_nou.png")
background = pygame.image.load("campo_futbol.png")

# Finestra del joc
size = (800,600)
screen = None

#Jugadors
jugadorA = Jugador(WHITE, 20, 100)
jugadorA.rect.x = 80
jugadorA.rect.y = 250

jugadorB = Jugador(WHITE, 20, 100)
jugadorB.rect.x = 700
jugadorB.rect.y = 250

#LLista de noms dels jugadors i variable on es guardara el guanyador
nom1 = '';
nom2 = '';
noms = [];
guanyador = '';

#Pilota
ball = Pilota(WHITE,20,20)
ball.rect.x = 380
ball.rect.y = 280

# Llista que tindra tots els Sprites del joc
all_sprites_list = pygame.sprite.Group()

# Afegir jugador al grup d'sprites
all_sprites_list.add(jugadorA)
all_sprites_list.add(jugadorB)
all_sprites_list.add(ball)

# Flags
inici_joc = True;
gameOn = True
game_over = False

# Un clock per controlar la vel. de refrescament de la pantalla
clock = pygame.time.Clock()

# Funcio format text
def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("courier", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

#Funcio Entrada Dades Usuari
def entrada_dades():
    nom1 = input("Nom del jugador 1: ");
    print("\nLoading...");
    time.sleep(1);
    nom2 = input("Nom del jugador 2: ");
    print("\nLoading...");
    time.sleep(1);
    print("\nA divertir-se!")
    noms.append(nom1);
    noms.append(nom2);
    return noms;

def video(path):
    cap = cv2.VideoCapture(path)
    player = MediaPlayer(path)
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        audio_frame, val = player.get_frame()

        if ret == True:
            frame = cv2.resize(frame, size, None)
            cv2.imshow('frame',frame)
            time.sleep(1/FPS) #1/60
            if val != 'eof' and audio_frame is not None:
                #audio
                img, t = audio_frame
            if cv2.waitKey(1) & 0xFF == ord(' '):
                cap.release()
                cv2.destroyAllWindows()
        else:
            cap.release()
            cv2.destroyAllWindows()

#Funcio menu principal
def pantalla_inici(nom_1, nom_2):
    waiting = True;
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pong by ALEXIS & POL")
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit();
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False;

        screen.fill(BLACK);

        draw_text(screen, "PONG PROJECTE SAD", 50, 400, 10);
        draw_text(screen, "Benvinguts/des", 40, 400, 200);
        draw_text(screen, nom_1 + " es mou amb 's' i 'w'", 32, 400, 310);
        draw_text(screen, nom_2 + " es mou amb les fletxes", 32, 400, 340);
        draw_text(screen, "Prem 'ENTER' per començar", 32, 400, 510);

        pygame.display.flip();
    return screen
        
# Funcio pantalla game over
def pantalla_gameover(screen):
    screen.blit(campnou, [0, 0]);
    s = pygame.mixer.Sound('Crowd.mp3')
    s.play()
    draw_text(screen, "PONG", 65, 400, 20)
    draw_text(screen, "Guanyador/a:", 50, 400, 150)
    draw_text(screen, guanyador, 50, 400, 225)
    draw_text(screen, "Press 'Enter' per reiniciar", 25, 400, 400)
    pygame.display.flip()
    waiting = True;
    while waiting:
        clock.tick(60);
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit();
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    s.stop()
                    waiting = False;
# Puntuacio Jugadors
scoreA = 0
scoreB = 0

#***********************************************************************
# -------- Bucle Programa Principal -----------
while gameOn:
    if inici_joc == True:
        path = "/Users/alexis/Desktop/PROJECTE PYGAME PONG_ALEXIS_NAVARRO_POL_FERNÁNDEZ/PONG_POL_ALEXIS/IntroVideo1.mp4"
        video(path)
        noms = entrada_dades()
        screen = pantalla_inici(noms[0], noms[1])
        inici_joc = False
        
    if game_over == True:
        pantalla_gameover(screen)
        #Resetegem TOT
        game_over = False;
        #Marcador
        scoreA = 0;
        scoreB = 0;
        #Coordenadas de la pilota
        ball.rect.x = 380
        ball.rect.y = 280


    # --- Bucle d'Events
    for event in pygame.event.get(): # Usuari fa alguna cosa
        if event.type == pygame.QUIT: # Si usuari prem Close
            gameOn = False # Flag per sortir del bucle
    

    #Moure els jugadors amb les fletxes (jugadorA) o "W/S" (jugadorB) 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        jugadorA.moveUp(6)
    if keys[pygame.K_s]:
        jugadorA.moveDown(6)
    if keys[pygame.K_UP]:
        jugadorB.moveUp(6)
    if keys[pygame.K_DOWN]:
        jugadorB.moveDown(6)
#***********************************************************************
    # --- Llogica del joc
    
    all_sprites_list.update()
    
    # Comprova si la pilota rebota en una de les 4 parets:
    if ball.rect.x>=780:
        scoreA += 1
        # compteEnrere()
        ball.rect.x = 380
        ball.rect.y = 280
        # Marcador
        if scoreA >= 5:
            guanyador = noms[0]
            game_over = True; #Gana el jugador A
        ball.velocity[0] = -ball.velocity[0]
    
    if ball.rect.x<=0:
        scoreB += 1
        # compteEnrere()
        ball.rect.x = 380
        ball.rect.y = 280
        if scoreB >= 5:
            guanyador = noms[1]
            game_over = True; #Gana el jugador B
        ball.velocity[0] = -ball.velocity[0]
    
    if ball.rect.y>580:
        ball.velocity[1] = -ball.velocity[1]
    
    if ball.rect.y<0:
        ball.velocity[1] = -ball.velocity[1] 
    
    # Detecta colisions entre la pilota i els jugadors
    if pygame.sprite.collide_mask(ball, jugadorA) or pygame.sprite.collide_mask(ball, jugadorB):
        ball.bounce()
        s = pygame.mixer.Sound('BallKick.mp3')
        s.play()

    # --- Dibuixos del joc

    # Resetejar fons de pantalla pantalla
    screen.blit(background, [0,0]);
    #Marcador
    draw_text(screen, noms[0] + ": " + str(scoreA)  + "   " + noms[1] + ": " + str(scoreB), 25, 400, 10)    
    
    # Dibuixar totes les sprites de cop!
    all_sprites_list.draw(screen) 

    # --- Actualitza la pantalla amb el que hem dibuixat
    pygame.display.flip()

    # --- Limita els fps a 60
    clock.tick(FPS)

#Fora del bucle principal, aturem el joc
pygame.quit()