# -*- coding: utf-8 -*-

import pygame
import math
import random

pygame.init() # initialisation du module "pygame"
pygame.mixer.init() #son
arial24 = pygame.font.SysFont("arial",24)
fenetre = pygame.display.set_mode( (1000,1000) ) # Création d'une fenêtre graphique de taille 600x600 pixels
pygame.display.set_caption("Napoleon  War") # Définit le titre de la fenêtre
record=0
def jouer():
    garde=pygame.image.load("Garde.png")
    garde=pygame.transform.scale(garde,(64,64))
    anglais=pygame.image.load("anglais.png")
    anglais=pygame.transform.scale(anglais,(64,64))
    cavalier=pygame.image.load("Cavalier.png")
    cavalier=pygame.transform.scale(cavalier,(64,64))
    fantassin=pygame.image.load("Fantassin.png")
    fantassin=pygame.transform.scale(fantassin,(64,64))
    nageurfrancais=pygame.image.load("nagefrancais.png")
    nageurfrancais=pygame.transform.scale(nageurfrancais,(64,64))
    nageuranglais=pygame.image.load("nageanglais.png")
    nageuranglais=pygame.transform.scale(nageuranglais,(64,64))
    arcole=pygame.image.load("arcole.jpg")
    arcole=pygame.transform.scale(arcole,(1000,1000))
    arrive=pygame.mixer.Sound("ils arrivent.wav")
    chargez=pygame.mixer.Sound("chargez.wav")
    aled=pygame.mixer.Sound("a l'aide.wav")
    infanterie=pygame.mixer.Sound("baionnette.wav")
    score=0
    nbproj=100
    projectile=[]
    joueur=(475,700)
    L=[]
    tir=False
    dis=0
    appui=False
    boutons = {
        "Facile": pygame.Rect(250, 800, 150, 50),
        "Moyen": pygame.Rect(425, 800, 150, 50),
        "Difficile": pygame.Rect(600, 800, 150, 50)
    }
    for i in range(0,800):
        for j in range(0,800):
            if not((i>=350 and i<=550) or (j>=350 and j<=550)):
                L.append((i,j))
    arbres=[L[random.randint(0,len(L)-1)] for i in range(random.randint(10,30))]
    diff=1
    ennemie=[]
    pont=[]
    for i in range(10000):
        a=random.randint(0,800)
        b=random.randint(0,300)
        ennemie.append((a,b))
        pont.append(False)
    fusil=(-1,-1)
    difficulte=None
    Gar=False
    Fant=True
    Cav=False
    def menu():
        nonlocal continuer, difficulte,arrive
        running=True
        while running:
            fenetre.fill((255,255,255))
            fenetre.blit(arcole,(0,0))
            titre = arial24.render("Bataille de l'ARCOLE", True, (0,0,0))
            fenetre.blit(titre, (400, 80))
            regles = [
                "Vous incarnerez dans ce jeu un fantassin mené par Napoléon puis un cavalier et finalement",
                "un soldat de la Vieille Garde!",
                "Les ennemis anglais arrivent par vagues. Éliminez-les !",
                " Objectif : Survivre et vaincre le maximum d'ennemi. Rendez fière la Grande Armée",
                "en maximisant votre record!",
                "Commandes : Z -> Avancer   Q -> Gauche   S -> Reculer   D -> Droite",
                "ESPACE : Tirer une balle",
                "Le fantassin a une vitesse de 5, le cavalier a une vitesse de 7 et le soldat de la Vieille Garde a une vitesse de 6",
                " Choisissez un niveau !",
                "Quel que soit le niveau choisi, si le fantassin est touché, il meurt!",
                "Niveau Facile: Vie du cavalier -> 70 / Vie du soldat de la garde -> 30 / Son nombre de balles -> 100",
                "Vitesse de l'ennemie -> 2",
                "Niveau Moyen: Vie du cavalier -> 60 / Vie du soldat de la garde -> 20 / Son nombre de balles -> 80",
                "Vitesse de l'ennemie -> 3",
                "Niveau Difficile: Vie du cavalier -> 40 / Vie du soldat de la garde -> 15 / Son nombre de balles -> 50",
                "Vitesse de l'ennemie -> 5",

            ]
            i=0
            for ligne in regles:
                texte = arial24.render(ligne, True,(0,0,0))
                fenetre.blit(texte, (20, 120 + i * 40))
                i+=1
            for nom, rect in boutons.items():
                pygame.draw.rect(fenetre, (200,200,200), rect)
                texte_bouton = arial24.render(nom, True, (0,0,0))
                texte_rect = texte_bouton.get_rect(center=rect.center)
                fenetre.blit(texte_bouton, texte_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for nom, rect in boutons.items():
                        if rect.collidepoint(event.pos):
                            difficulte = nom
                            running = False
                            arrive.play()

    def distance(a,b):
        return math.sqrt((a)**2+(b)**2)

    def bataille():
        fenetre.fill((85, 135, 60))
        
        for i in range(len(arbres)):
            pygame.draw.circle(fenetre,(34,85,28),arbres[i],7)
        pygame.draw.rect(fenetre, (210, 180, 140), (425, 0, 150, 1000)) #chemin
        riviere = pygame.Rect(0, 450, 1000, 100) #riviere
        pygame.draw.rect(fenetre, (30, 144, 255), riviere)
        pont = pygame.Rect(430,450, 140, 100) #pont
        pygame.draw.rect(fenetre, (205, 133, 63), pont)
        if Fant:
            if fusil!=(-1,-1):
                pygame.draw.circle(fenetre,(0,0,0),fusil,3)
            if (0<=joueur[0]<=420 or 550<=joueur[0]<=1000) and(420<=joueur[1]<=500):
                fenetre.blit(nageurfrancais,joueur)
            else:
                fenetre.blit(fantassin,joueur) #joueur
        if Cav:
            if (0<=joueur[0]<=420 or 550<=joueur[0]<=1000) and(420<=joueur[1]<=500):
                fenetre.blit(nageurfrancais,joueur)
            else:
                fenetre.blit(cavalier,joueur) #joueur
            vie1=arial24.render("Vie: "+ str(viecav),True,(0,0,0))
            fenetre.blit(vie1,(800,750))
        if Gar:
            if (0<=joueur[0]<=420 or 550<=joueur[0]<=1000) and(420<=joueur[1]<=500):
                fenetre.blit(nageurfrancais,joueur)
            else:
                fenetre.blit(garde,joueur) #joueur
            for i in range(len(projectile)):
                pygame.draw.circle(fenetre,(0,0,0),projectile[i],3)
            proj=arial24.render("Projectiles: "+str(nbproj),True,(0,0,0))
            vie2=arial24.render("Vie: " + str(viegarde),True,(0,0,0))
            fenetre.blit(proj,(40,750))
            fenetre.blit(vie2,(800,750))
        for i in range(diff):
            if (0<=ennemie[i][0]<=420 or 550<=ennemie[i][0]<=1000) and (420<=ennemie[i][1]<=500):
                fenetre.blit(nageuranglais,ennemie[i])
            else:
                fenetre.blit(anglais,ennemie[i]) #ennemie
        s=arial24.render("Score : "+ str(score),True,(0,0,0))
        fenetre.blit(s,(450,50))
        pygame.display.flip()
    
    clock = pygame.time.Clock()

    def deplacementjoueur():
        nonlocal continuer,joueur
        touches = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Permet de gérer un clic sur le bouton de fermeture de la fenêtre
                continuer = 0
        if touches[pygame.K_s] == True and joueur[1] <= 990:
            joueur = (joueur[0], joueur[1] + vjoueur)

        if touches[pygame.K_z] == True and joueur[1] >= 10:
            joueur = (joueur[0], joueur[1] - vjoueur)

        if touches[pygame.K_q] == True and joueur[0] >= 10:
            joueur = (joueur[0] - vjoueur, joueur[1])

        if touches[pygame.K_d] == True and joueur[0] <= 990:
            joueur = (joueur[0] + vjoueur, joueur[1])
        
    def deplacementennemi():
        nonlocal ennemie,joueur
        for i in range(diff):
            if pont[i]==False:
                if ennemie[i][0]<=450:
                    ennemie[i]=(ennemie[i][0]+vennemie,ennemie[i][1])
                elif ennemie[i][0]>=520:
                    ennemie[i]=(ennemie[i][0]-vennemie,ennemie[i][1])
                elif ennemie[i][0]>=450 and ennemie[i][0]<=520 and ennemie[i][1]<=600:
                    ennemie[i]=(ennemie[i][0],ennemie[i][1]+vennemie)
                else:
                    pont[i]=True
                    x=joueur[0]-ennemie[i][0]
                    y=joueur[1]-ennemie[i][1]
                    d=distance(x,y)
                    if d!=0:
                        x=x/d
                        y=y/d
                    ennemie[i]=(ennemie[i][0]+vennemie*x,ennemie[i][1]+vennemie*y)
            else:
                x=joueur[0]-ennemie[i][0]
                y=joueur[1]-ennemie[i][1]
                d=distance(x,y)
                if d!=0:
                    x=x/d
                    y=y/d
                ennemie[i]=(ennemie[i][0]+vennemie*x,ennemie[i][1]+vennemie*y)
    def tirfusil():
        nonlocal ennemie,fusil,score,tir,dis,nbproj,projectile,appui
        touches = pygame.key.get_pressed()
        if Fant:
            if tir:
                fusil=(fusil[0],fusil[1]-vjoueur)
                dis+=vjoueur
                balle=pygame.Rect(fusil,(3,3))
                if fusil!=(-1,-1):
                    for i in range(diff):
                        adv=pygame.Rect(ennemie[i],(40,40))
                        if adv.colliderect(balle):
                            ennemie.pop(i)
                            pont.pop(i)
                            fusil=(-1,-1)
                            tir=False
                            score+=1
                            dis=0
                            break
                if dis>=500:
                    tir=False
                    fusil=(-1,-1)
                    dis=0
            else:   
                if touches[pygame.K_SPACE]==True :
                    tir=True
                    fusil=(joueur[0]+30,joueur[1]+15)
                    dis=0
        if Gar:
            if touches[pygame.K_SPACE] == False:
                appui=False
            if touches[pygame.K_SPACE]==True and appui==False and nbproj>0:
                for i in range(len(projectile)):
                    if projectile[i]==(-1,-1):
                        projectile[i]=(joueur[0]+30,joueur[1]+15)
                        nbproj-=1
                        break
                appui=True
            for i in range(len(projectile)):
                if projectile[i]!=(-1,-1):
                    projectile[i]=(projectile[i][0],projectile[i][1]-vjoueur)
    continuer=0
    while continuer!=1:
        menu()
        if difficulte!=None:
            continuer=1
            break
    # ici on va mettre les parametres pour facile/moyen/difficile
    vjoueur=5
    viecav=70
    viegarde=30
    vennemie=0
    if difficulte=="Facile":
        vennemie=2
        viecav=70
        viegarde=30
        nbproj=100
    elif difficulte=="Moyen":
        vennemie=3
        viecav=60
        viegarde=20
        nbproj=80
    else:
        vennemie=5
        viecav=40
        viegarde=15
        nbproj=50
    projectile=[(-1,-1) for i in range(nbproj)]
    ajout=False

    while continuer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = 0
        bataille()
        deplacementjoueur()
        deplacementennemi()
        tirfusil() 
        player=pygame.Rect(joueur,(40,40))
        if Fant:
            for i in range(diff):
                adv=pygame.Rect(ennemie[i],(40,40))
                if adv.colliderect(player):
                    ennemie.pop(i)
                    pont.pop(i)
                    Fant=False
                    Cav=True
                    chargez.play()
                    joueur=(475,700)
        if Cav:
            vjoueur=7
            if viecav>0:
                for i in range(diff):
                    adv=pygame.Rect(ennemie[i],(40,40))
                    if adv.colliderect(player):
                        viecav-=1
                        score+=1
                        ennemie.pop(i)
                        pont.pop(i)
                        break
            else:
                Cav=False
                Gar=True
                infanterie.play()
                joueur=(475,700)
        if Gar:
            vjoueur=6
            for i in range(len(projectile)):
                balle=pygame.Rect(projectile[i],(3,3))
                for i in range(diff):
                    adv=pygame.Rect(ennemie[i],(40,40))
                    if balle.colliderect(adv):
                        score+=1
                        ennemie.pop(i)
                        pont.pop(i)
                        projectile[i]=(-1,-1)
                        break
            if viegarde>0:
                for i in range(diff):
                    adv=pygame.Rect(ennemie[i],(40,40))
                    if adv.colliderect(player):
                        ennemie.pop(i)
                        pont.pop(i)
                        score+=1
                        viegarde-=1
                        break
            else:
                aled.play()
                return score
        if score%5!=0:
            ajout=True
        elif score%5==0 and score!=0 and ajout:
            diff+=1
            ajout=False
        clock.tick(50)

def gameover(score):
    global record,continuer
    if score > record:
        record = score
    bouton_restart = pygame.Rect(400, 600, 200, 50)
    restart = False
    while not restart:
        fenetre.fill((0, 0, 0))
        texte = arial24.render("GAME OVER", True, (255, 0, 0))
        texte_score = arial24.render("Score : "+str(score), True, (255, 255, 255))
        texte_record = arial24.render("Record : "+str(record), True, (255, 255, 0))
        texte_bouton = arial24.render("Recommencer", True, (0, 0, 0))
        pygame.draw.rect(fenetre, (200, 200, 200), bouton_restart)
        texte_rect = texte_bouton.get_rect(center=bouton_restart.center)
        fenetre.blit(texte, (425, 300))
        fenetre.blit(texte_score, (425, 360))
        fenetre.blit(texte_record, (425, 400))
        fenetre.blit(texte_bouton, texte_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer=0
                restart = True
            elif event.type == pygame.MOUSEBUTTONDOWN and bouton_restart.collidepoint(event.pos):
                restart = True
        pygame.display.flip()
score=0

while True:
    score=jouer()
    gameover(score)
