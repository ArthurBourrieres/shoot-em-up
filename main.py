import pygame
from random import randint


pygame.init()

L_scr = 720
l_scr = 1300

L_player = 50
l_player = 50

SCR =pygame.display.set_mode((l_scr, L_scr))
Clock = pygame.time.Clock()
font = pygame.font.SysFont("Segoe", 40 )


img_météore = pygame.image.load("météore.png")
img_météore = pygame.transform.scale(img_météore, (50, 50))

img_veseau = pygame.image.load("veseau.png")
img_veseau = pygame.transform.scale(img_veseau, (l_player, L_player))

img_enemie = pygame.image.load("enemie.png")
img_enemie = pygame.transform.scale(img_enemie, (50, 50))

x_player = 100
y_player = 400

chaleur = 0


run = True
vivant = True
tir_traversant = False
tir_multiple = False

missile_ennemie = []
missile = []
ennemie = []
météor = []
étoile = []
bonus_liste = []

moov = 2
conteur = 0
spone = 3
spone_météor_viser = 5
spone_météor = 2
temps = 3
nombre_enemie = 1
conteur_enemie = 0
tranche_dix = 10
ennemie_eliminé = 0

first_run = True

bosse = False

bosse1 = False
bosse1_vaincu = False
bosse1_vie = 100
bosse1_x = 400
bosse1_y = 50
moov_boss1 = 3


while run:
    chaleur -= 0.03
    S = conteur / 60
    Keys = pygame.key.get_pressed()
    SCR.fill('black')
    conteur += 1

    # écrit le score
    text = font.render(str(ennemie_eliminé), True, "white")
    SCR.blit(text, (50, 55))




#étoile
    #apparition des premiers étoile
    if first_run:
        nombre_étoile = 0
        while nombre_étoile != 160:
            x_étoile = randint(0, l_scr)
            y_étoile = randint(0, L_scr)
            étoile_taille = randint(2, 6)
            étoile.append([x_étoile, y_étoile, étoile_taille])
            nombre_étoile += 1

    #gere l'apparition des étoile et leur déplacement
    for i in étoile:
        i[1] += i[2]/5
        pygame.draw.circle(SCR, 'white', [i[0], i[1]], i[2])
        if i[1] > L_scr:
            étoile.remove(i)
            x_étoile = randint(0, l_scr)
            y_étoile = randint(-10, 0)
            étoile_taille = randint(2, 6)
            étoile.append([x_étoile, y_étoile, étoile_taille])

    pygame.draw.rect(SCR, 'green', [90, 57, 160, 20])
    pygame.draw.rect(SCR, 'red', [90, 60, chaleur * 10, 15])


#joueur
    #affiche le joueur
    #pygame.draw.rect(SCR, 'green', [x_player, y_player, L_player, l_player])
    SCR.blit(img_veseau, (x_player, y_player))

    #permet les deplacement du joueur
    if vivant:
        if Keys[pygame.K_UP]:
            y_player -= 10
        if Keys[pygame.K_DOWN]:
            y_player += 10
        if Keys[pygame.K_LEFT]:
            x_player -= 10
        if Keys[pygame.K_RIGHT]:
            x_player += 10

    #empeche le joueur de sortir
    if y_player >= L_scr:
        y_player = 590
    if y_player <= 0:
        y_player = 10
    if x_player >= l_scr:
        x_player = 790
    if x_player <= 0:
        x_player = 10

    #gere les missile du joueur
    for i in missile:
        x = i[0]
        y = i[1]
        i[1] -= 10
        pygame.draw.rect(SCR, 'red', [x, y, 5, 30])
        if not 0 < i[1] < L_scr:
            missile.remove(i)


#ennemie
    # gére l'apparition des ennemie
    if vivant and not bosse:
        if len(ennemie) == 0:
            conteur_enemie = 0
            while conteur_enemie != nombre_enemie:
                x_en = randint(10, 790 )
                y_en = randint(10, 300)
                type_ennemie = randint(1, 2)
                print(type_ennemie)
                if type_ennemie == 1:
                    moov = randint(-5, 5)
                    ennemie.append([x_en, y_en, type_ennemie, moov])

                if type_ennemie == 2:
                    vecteur_x = randint(-4, 4)
                    vecteur_Y = randint(-4, 4)
                    ennemie.append([x_en, y_en, type_ennemie, vecteur_x, vecteur_Y])


                conteur_enemie += 1
            nombre_enemie += 1



    #gere les ennemie
    for i in ennemie:

        if i[2] == 1:
            x = i[0]
            y = i[1]
            # pygame.draw.rect(SCR, 'white', [x, y, 30, 30])
            SCR.blit(img_enemie, (x, y))
            i[0] += i[3]
            if not 0 < i[0] < l_scr:
                i[3] *= -1

        if i[2] == 2:
            i[0] += i[3]
            i[1] += i[4]
            if not 0 < i[0] < l_scr:
                i[3] *= -1
            if not 0 < i[1] < L_scr:
                i[4] *= -1
            SCR.blit(img_enemie, (i[0], i[1]))



        spone_missile = randint(1, 500)
        if spone_missile == 1:
            missile_ennemie.append([i[0]+15, i[1]+15])

    #gere les colition missile sur ennemie et l'apparition des bonus
    for a in missile:
        for i in ennemie:
            if i[0] <= a[0] <= i[0] + 50 and i[1] <= a[1] <= i[1] + 30:
                ennemie.remove(i)
                ennemie_eliminé += 1
                bonus = randint(1, 50)
                if bonus == 1:
                    bonus_liste.append([i[0], i[1], bonus])
                if not tir_traversant:
                    missile.remove(a)
                if bonus == 2:
                    bonus_liste.append([i[0], i[1], bonus])
                break

    #gére les colitions ennemies joueur
    for i in ennemie:
        if x_player+10 <= i[0] <= x_player + l_player-10 and y_player <= i[1] <= y_player + l_player:
            vivant = False
            ennemie.remove(i)
        if x_player+10 <= i[0]+ 50 <= x_player + l_player-10 and y_player <= i[1] <= y_player + l_player:
            vivant = False
            ennemie.remove(i)
        if x_player+10 <= i[0] + 15 <= x_player + l_player-10 and y_player <= i[1] + 50 <= y_player + l_player:
            vivant = False
            ennemie.remove(i)
        if x_player+10 <= i[0] + 35 <= x_player + l_player-10 and y_player <= i[1] + 50 <= y_player + l_player:
            vivant = False
            ennemie.remove(i)

    # gere les colitions des missiles ennemies sur joueur
    for i in missile_ennemie:

        if x_player + 10 <= i[0] + 3 <= x_player + l_player - 10 and y_player <= i[1] + 30 <= y_player + l_player:
            vivant = False

    # gére les missile ennemie
    for i in missile_ennemie:
        x1 = i[0]
        y1 = i[1]
        i[1] += 5
        pygame.draw.rect(SCR, 'yellow', [x1, y1, 5, 30])


#météor
    # fait apparait les météore
    if vivant and not bosse:
        if S > spone_météor_viser:
            météor.append([x_player, y_player - 700])
            spone_météor_viser += 5
        if S == spone_météor:
            spone_météor += 2

            x_météor_al = randint(0, 800)
            y_météor_al = randint(-100, -50)
            météor.append([x_météor_al, y_météor_al])

    #gére les météore
    for i in météor:
        x_météor = i[0]
        y_météor = i[1]
        i[1] += 5
        #pygame.draw.rect(SCR, 'red', [x_météor, y_météor, 30, 30])
        SCR.blit(img_météore, (x_météor, y_météor))

    #gere les colition des météores
    for i in météor:
        if i[0] + 10 <= x_player+25 <= i[0] + 40 and i[1] <= y_player <= i[1] + 30 or x_player <= i[0]+25 <= x_player + 30 and y_player <= i[1] <= y_player + 30:
            vivant = False

    #empeche les missiles de passer à travers les météors
    for i in météor:
        for a in missile:
            if i[0] <= a[0] <= i[0] + 30 and i[1] <= a[1] <= i[1] + 30:
                missile.remove(a)


#bonus
    # donne les effet des bonus
    for i in bonus_liste:
        i[1] += 3
        pygame.draw.rect(SCR, 'red', [i[0], i[1], 20, 20])
        if i[2] == 1:
            if x_player <= i[0] <= x_player + l_player - 10 and y_player <= i[1] <= y_player + l_player:
                tir_traversant = True
                bonus_liste.remove(i)
        if i[2] == 2:
            if x_player <= i[0] <= x_player + l_player - 10 and y_player <= i[1] <= y_player + l_player:
                tir_multiple = True
                bonus_liste.remove(i)

#mort
    #definie l'état de mort
    if not vivant:
        img_veseau = pygame.image.load("explotion.png")
        img_veseau = pygame.transform.scale(img_veseau, (50, 50))
        text_perdu = font.render("Vous avez perdue, votre score est de: " + str(ennemie_eliminé), True, "white")
        SCR.blit(text_perdu, (20, 100))


#permet de tirer les missiles est de fermer la fenétre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if vivant and chaleur <= 15:
                if event.key == pygame.K_SPACE:
                    chaleur += 1
                    missile.append([x_player + 25, y_player - 20])
                    if tir_multiple:
                        missile.append([x_player, y_player - 20])
                        missile.append([x_player + 50, y_player - 20])
            if event.key == pygame.K_a:
                ennemie.append([x_player, y_player-400])

#permmet de restart
    if Keys[pygame.K_z]:
        ennemie = []
        missile = []
        missile_ennemie = []
        bonus_liste = []
        vivant = True
        conteur = 0
        S = 0
        nombre_enemie = 1
        conteur_enemie = 0
        spone = 3
        tranche_dix = 10
        ennemie_eliminé = 0
        spone_météor = 3
        chaleur = 0
        tir_traversant = False
        tir_multiple = False
        img_veseau = pygame.image.load("veseau.png")
        img_veseau = pygame.transform.scale(img_veseau, (l_player, L_player))



#bos
    #fait apparaitre le bos
    if ennemie_eliminé >= 150 and not bosse1_vaincu:
        bosse1 = True
        bosse = True

    #gere le bos
    if bosse1 == True:
        pygame.draw.rect(SCR, 'green', [bosse1_x, bosse1_y, 100, 100])
        bosse1_x += moov_boss1
        if not 0 < bosse1_x < L_scr or not 0 < bosse1_x + l_scr < 600:
            moov_boss1 *= -1
        tir_bosse = randint(1, 50)
        if tir_bosse == 1:
            missile_ennemie.append([bosse1_x, bosse1_y])
            missile_ennemie.append([bosse1_x+ 50, bosse1_y])
            missile_ennemie.append([bosse1_x + 100, bosse1_y])

    #tire les missiles
        for i in missile:
            if bosse1_x <= i[0] <= bosse1_x + 100 and bosse1_y <= i[1] <= bosse1_y + 100:
                bosse1_vie -= 1
                missile.remove(i)

    #gere la mort du bos
        if bosse1_vie < 0:
            bosse = False
            bosse1 = False
            bosse1_vaincu = True

    pygame.display.flip()

    first_run = False

    delta_t = Clock.tick(60)