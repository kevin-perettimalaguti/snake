import random

class IA:
    def __init__(self, jeu):
        self.jeu = jeu
        self.directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Up, Down, Left, Right

    def choisir_direction(self):
        tete_x, tete_y = self.jeu.serpent.corps[0]
        nourriture_x, nourriture_y = self.jeu.nourriture.position

        # Calcul des différences en x et y entre la tête et la nourriture
        diff_x = nourriture_x - tete_x
        diff_y = nourriture_y - tete_y

        # Logique de décision de l'IA basée sur la position de la tête et de la nourriture
        if diff_x > 0:
            return (1, 0)  # Aller vers la droite
        elif diff_x < 0:
            return (-1, 0)  # Aller vers la gauche
        elif diff_y > 0:
            return (0, 1)  # Aller vers le bas
        elif diff_y < 0:
            return (0, -1)  # Aller vers le haut
        else:
            # Si la tête est alignée avec la nourriture, choisis une direction aléatoire
            return random.choice(self.directions)

    def jouer(self):
        direction = self.choisir_direction()
        self.jeu.serpent.direction = direction
