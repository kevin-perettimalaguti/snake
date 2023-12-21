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
        if diff_x > 0 and (tete_x + 1, tete_y) not in self.jeu.serpent.corps[1:]:
            return (1, 0)  # Aller vers la droite
        elif diff_x < 0 and (tete_x - 1, tete_y) not in self.jeu.serpent.corps[1:]:
            return (-1, 0)  # Aller vers la gauche
        elif diff_y > 0 and (tete_x, tete_y + 1) not in self.jeu.serpent.corps[1:]:
            return (0, 1)  # Aller vers le bas
        elif diff_y < 0 and (tete_x, tete_y - 1) not in self.jeu.serpent.corps[1:]:
            return (0, -1)  # Aller vers le haut
        else:
            # Si la tête est alignée avec la nourriture, évite les zones dangereuses
            return self.eviter_zones_dangereuses()

    def esquiver_bords(self):
        tete_x, tete_y = self.jeu.serpent.corps[0]
        directions_disponibles = []

        # Vérifie les directions disponibles pour éviter les bords
        if tete_x > 0 and (tete_x - 1, tete_y) not in self.jeu.serpent.corps[1:]:
            directions_disponibles.append((-1, 0))  # Gauche
        if tete_x < self.jeu.nombre_cases - 1 and (tete_x + 1, tete_y) not in self.jeu.serpent.corps[1:]:
            directions_disponibles.append((1, 0))  # Droite
        if tete_y > 0 and (tete_x, tete_y - 1) not in self.jeu.serpent.corps[1:]:
            directions_disponibles.append((0, -1))  # Haut
        if tete_y < self.jeu.nombre_cases - 1 and (tete_x, tete_y + 1) not in self.jeu.serpent.corps[1:]:
            directions_disponibles.append((0, 1))  # Bas

        # Choisi une direction aléatoire parmi celles disponibles
        return random.choice(directions_disponibles)

    def eviter_zones_dangereuses(self):
        tete_x, tete_y = self.jeu.serpent.corps[0]
        directions_disponibles = []

        # Vérifie les directions disponibles pour éviter les zones dangereuses
        for direction in self.directions:
            prochaine_position = (tete_x + direction[0], tete_y + direction[1])

            # Évite les positions à proximité des bords
            if (
                prochaine_position[0] > 1
                and prochaine_position[0] < self.jeu.nombre_cases - 2
                and prochaine_position[1] > 1
                and prochaine_position[1] < self.jeu.nombre_cases - 2
                and prochaine_position not in self.jeu.serpent.corps[1:]
            ):
                directions_disponibles.append(direction)

        # Choisi une direction aléatoire parmi celles disponibles
        return random.choice(directions_disponibles)

    def jouer(self):
        direction = self.choisir_direction()
        self.jeu.serpent.direction = direction