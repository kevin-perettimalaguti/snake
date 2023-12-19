# Importation des modules
import pygame, random, pygame_menu

# Initiation de pygame
pygame.init()

# Police
police_titre = pygame.font.Font(None, 60)
police_score = pygame.font.Font(None, 40)

# Couleur de jeu
VERT = (173, 204, 96)
VERT_FONCE = (43, 51, 24)
BLACK = (22, 5, 11)
ROUGE = (235, 0, 41)

# Dimension des cases
taille_case = 25
nombre_cases = 20

DECALAGE = 75

# Définition de la fenêtre principale
ecran = pygame.display.set_mode((2 * DECALAGE + taille_case * nombre_cases, 2 * DECALAGE + taille_case * nombre_cases))
pygame.display.set_caption("Snake")

# ====================MES CLASSES=====================
class Nourriture:
    def __init__(self, corps_serpent):
        self.position = self.generer_position_aleatoire(corps_serpent)

    def dessiner(self):
        rect_nourriture = pygame.Rect(DECALAGE + self.position[0] * taille_case, DECALAGE + self.position[1] * taille_case,
                                       taille_case, taille_case)
        ecran.blit(surface_nourriture, rect_nourriture)

    def generer_case_aleatoire(self):
        x = random.randint(0, nombre_cases - 1)
        y = random.randint(0, nombre_cases - 1)
        return x, y

    def generer_position_aleatoire(self, corps_serpent):
        position = self.generer_case_aleatoire()
        while position in corps_serpent:
            position = self.generer_case_aleatoire()
        return position

class Serpent:
    def __init__(self):
        self.corps = [(6, 9), (5, 9), (4, 9)]
        self.direction = (1, 0)
        self.ajouter_segment = False
        self.son_manger = pygame.mixer.Sound("Sounds/eat.mp3")
        self.son_collision_mur = pygame.mixer.Sound("Sounds/wall.mp3")    

    def dessiner(self):
        for segment in self.corps:
            rect_segment = (DECALAGE + segment[0] * taille_case, DECALAGE + segment[1] * taille_case, taille_case,
                            taille_case)
            pygame.draw.rect(ecran, VERT_FONCE, rect_segment, 0, 7)

    def mettre_a_jour(self):
        self.corps.insert(0, (self.corps[0][0] + self.direction[0], self.corps[0][1] + self.direction[1]))
        if self.ajouter_segment:
            self.ajouter_segment = False
        else:
            self.corps = self.corps[:-1]

    def reinitialiser(self):
        self.corps = [(6, 9), (5, 9), (4, 9)]
        self.direction = (1, 0)

class Jeu:
    def __init__(self):
        self.serpent = Serpent()
        self.nourriture = Nourriture(self.serpent.corps)
        self.etat = "EN_COURS"
        self.score = 0

    def dessiner(self):
        self.nourriture.dessiner()
        self.serpent.dessiner()

    def mettre_a_jour(self):
        if self.etat == "EN_COURS":
            self.serpent.mettre_a_jour()
            self.verifier_collision_avec_nourriture()
            self.verifier_collision_avec_bords()
            self.verifier_collision_avec_queue()
    
    def verifier_collision_avec_bords(self):
        if self.serpent.corps[0][0] == nombre_cases or self.serpent.corps[0][0] == -1:
            self.partie_terminee()
        if self.serpent.corps[0][1] == nombre_cases or self.serpent.corps[0][1] == -1:
            self.partie_terminee()

    def partie_terminee(self):
        self.serpent.reinitialiser()
        self.nourriture.position = self.nourriture.generer_position_aleatoire(self.serpent.corps)
        self.etat = "ARRETE"
        self.score = 0
        self.serpent.son_collision_mur.play()              

    def verifier_collision_avec_queue(self):
        queue_sans_tete = self.serpent.corps[1:]
        if self.serpent.corps[0] in queue_sans_tete:
            self.partie_terminee()            

    def verifier_collision_avec_nourriture(self):
        if self.serpent.corps[0] == self.nourriture.position:
            self.nourriture.position = self.nourriture.generer_position_aleatoire(self.serpent.corps)
            self.serpent.ajouter_segment = True
            self.score += 1
            self.serpent.son_manger.play()      

jeu = Jeu()
surface_nourriture = pygame.image.load("Graphics/food.png")

MISE_A_JOUR_SERPENT = pygame.USEREVENT
pygame.time.set_timer(MISE_A_JOUR_SERPENT, 200)

# /////////////////////====================MENU====================\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Importer la classe Theme
from pygame_menu.themes import Theme

# Personnalisation des couleurs de mon menu
def afficher_menu():
    theme_vert_personnalise = Theme(background_color=(117, 180, 87),  # Ta nuance de vert
                                    title_background_color=BLACK,
                                    title_font_color=(255, 255, 255))  # Couleur du texte du titre

    # Utiliser le thème personnalisé lors de la création du menu
    menu = pygame_menu.Menu('SNAKE', 2 * DECALAGE + taille_case * nombre_cases, 2 * DECALAGE + taille_case * nombre_cases, theme=theme_vert_personnalise)
    # Ajout des boutons
    menu.add.button("PLAY", lambda: playing())
    menu.add.button("FAIRE JOUER L'IA")
    menu.add.button('LEAVE', pygame_menu.events.EXIT)

    return menu  # Retourne le menu créé

# /////////////////////====================FONCTION PRINCIPALE DU JEU=====================\\\\\\\\\\\\\\\\\\\\\\
def playing():
    # //////////////////====================BOUCLE PRINCIPALE=====================\\\\\\\\\\\\\\\\\\\\\\
    while 1:
        for evenement in pygame.event.get():
            if evenement.type == MISE_A_JOUR_SERPENT:
                jeu.mettre_a_jour()
            if evenement.type == pygame.QUIT:
                pygame.quit()

            if evenement.type == pygame.KEYDOWN:
                if jeu.etat == "ARRETE":
                    jeu.etat = "EN_COURS"
                if evenement.key == pygame.K_ESCAPE:
                    return afficher_menu()
                if evenement.key == pygame.K_UP and jeu.serpent.direction != (0, 1):
                    jeu.serpent.direction = (0, -1)
                if evenement.key == pygame.K_DOWN and jeu.serpent.direction != (0, -1):
                    jeu.serpent.direction = (0, 1)
                if evenement.key == pygame.K_LEFT and jeu.serpent.direction != (1, 0):
                    jeu.serpent.direction = (-1, 0)
                if evenement.key == pygame.K_RIGHT and jeu.serpent.direction != (-1, 0):
                    jeu.serpent.direction = (1, 0)

        # Dessin
        ecran.fill(VERT)
        pygame.draw.rect(ecran, VERT_FONCE,
                        (DECALAGE - 5, DECALAGE - 5, taille_case * nombre_cases + 10, taille_case * nombre_cases + 10), 5)
        jeu.dessiner()
        surface_titre = police_titre.render("Rétro Snake", True, VERT_FONCE)
        surface_score = police_score.render(str(jeu.score), True, VERT_FONCE)
        ecran.blit(surface_titre, (DECALAGE - 5, 20))
        ecran.blit(surface_score, (DECALAGE - 5, DECALAGE + taille_case * nombre_cases + 10))
        
        def game_over():
            VRAI = True
            game_loose = "Game Over"
            escape = "Press 'Escape' to return"
            end_score = f"Nombres de pommes mangées : {jeu.score}"
            font_perdu = pygame.font.SysFont("arial", 110)
            font_retour = pygame.font.SysFont("arial", 27)
            font_score = pygame.font.SysFont("arial", 32)
            ecran.fill(BLACK)
            if jeu.etat == "ARRETE":                
                affichage_perdu = font_perdu.render(game_loose, VRAI, ROUGE)
                ecran.blit(affichage_perdu, (90, 180))
                affichage_retour = font_retour.render(escape, VRAI, ROUGE)
                ecran.blit(affichage_retour, (210, 420))
                affichage_score = font_score.render(end_score, VRAI, (222, 54, 189))
                ecran.blit(affichage_score, (120, 320))
                pygame.display.update()

        # Afficher l'écran de game over si la partie est terminée
        if jeu.etat == "ARRETE":
            game_over()

        horloge = pygame.time.Clock()
        fps = 200
        horloge.tick(fps)
        pygame.display.update()

# Exécute la boucle du menu
afficher_menu().mainloop(ecran)
