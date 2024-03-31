from numpy import *
from random import *
from pygame import *
from math import *
from time import *
from matplotlib import *
import pylab as py
import pygame

""" Dans la représentation de la route choisie :
0 représente une partie de la route
1 représente une voiture
2 représente le décors
"""


def moyenne(L):
    """
    renvoie la moyenne des nombres compris dans la liste L
    """
    s = 0
    for k in range(0, len(L)):
        s += L[k]
    return (s / len(L))


def position_voiture(i, numéro_de_la_voie, carte):
    """
    Renvoie la position de la voiture i
    """
    map = carte.copy()
    k = numéro_de_la_voie
    # On cherche la position de la voiture i dans la voie k
    cpt, l = 0, 0
    while cpt != i:
        if map[k, l] == 1:
            cpt += 1
        if cpt != i:
            l += 1
        if l == map.shape[1]:
            return ("pas de voiture", i, " dans cette voie")
    return (l)


def position_fin_route(carte, voie):
    """
    Renvoie la position de la fin de la route
    """
    return len(carte[voie] - 1)


def peut_avancer(i, v, numéro_de_la_voie, carte):
    """
    Renvoie True si la voiture i peut avancer de v cases
    Renvoie False si non
    """
    map = carte.copy()
    k = numéro_de_la_voie
    l = position_voiture(i, k, map)

    if 1 not in [map[k, p] for p in range(l + 1, l + v + 1)]:
        return True
    else:
        return False


def peut_changer_de_voie(i, v, voie, carte, h_b):
    """
    Renvoie True si la voiture i peut changer de voie, en haut si h_b='h' ou en bas si h_b='b'
    """
    if nombre_de_voiture(carte, voie) == 1 and position_voiture(i, voie, carte) in [len(carte[0]) - k for k in
                                                                                    range(0, v)]:
        return False
    if h_b == 'b':
        l = position_voiture(i, voie, carte)
        if carte[voie + 1, l] == 2:
            return False
        if fin_dela_route(i, v, carte, voie):
            return False
        if 1 not in [carte[voie + 1, p] for p in range(l + 1, l + v + 1)] and 5 not in [carte[voie + 1, p] for p in
                                                                                        range(l + 1, l + v + 1)]:
            return True
        return False

    if h_b == 'h':
        l = position_voiture(i, voie, carte)
        if carte[voie - 1, l] == 2:
            return False
        if fin_dela_route(i, v, carte, voie):
            return False
        if 1 not in [carte[voie - 1, p] for p in range(l + 1, l + v + 1)] and 5 not in [carte[voie - 1, p] for p in
                                                                                        range(l + 1, l + v + 1)]:
            return True
        return False


def changer_de_voie(i, v, voie, carte, h_b):
    """
    La voiture i change voie de toujours une case en diagonale en haut ou en bas
    """
    l = position_voiture(i, voie, carte)
    if h_b == 'b':
        if carte[voie + 1, l + 1] == 1:
            return carte  # "sécurité" au cas où il y aurait déjà une voiture à la place où on souhaite changer de voie
        carte[voie, l] = 0
        carte[voie + 1, l + 1] = 1
    if h_b == 'h':
        if carte[voie - 1, l + 1] == 1:
            return carte
        carte[voie, l] = 0
        carte[voie - 1, l + 1] = 1
    return carte


def avancer(i, v, numéro_de_la_voie, carte):
    """
    fait avancer la voiture i
    """
    if not peut_avancer(i, v, numéro_de_la_voie, carte):
        return ("la voiture ne peut pas avancer")
    k = numéro_de_la_voie
    if peut_avancer(i, v, numéro_de_la_voie, carte):
        l = position_voiture(i, numéro_de_la_voie, carte)
        carte[k, l] = 0
        carte[k, l + v] = 1
    return carte


def fin_dela_route(i, v, carte, numéro_de_la_voie):
    """
    Renvoie True si la voiture est entre la fin de la route et fin de la route - v
    Renvoie False si non
    """
    fin = carte.shape[1]
    l = position_voiture(i, numéro_de_la_voie, carte)
    if l in [s for s in range(fin - v, fin + 1)]:
        return True
    return False


def nombre_de_voiture(carte, voie):
    """
    Renvoie le nombre de voiture présentent sur la carte
    """
    cpt = 0
    for k in range(0, carte.shape[1]):
        if carte[voie, k] == 1:
            cpt += 1
    return cpt


def ajouterunevoiture(carte, voie):
    """
    ajoute une voiture au début de la route
    """
    carte[voie, 0] = 1
    return carte


def distance_v(i, carte, voie):
    """
    renvoie la distance entre la voiture i et la voiture i+1
    """
    pos1 = position_voiture(i, voie, carte)
    if i != nombre_de_voiture(carte, voie):
        pos2 = position_voiture(i + 1, voie, carte)
        return (pos2 - pos1 - 1)
    else:
        return position_fin_route(carte, voie) - pos1


def pliage(Carte):
    """
    Prend en argument une carte de longueur de format 1x36 et renvoie une carte en forme de boucle pour effecteur l'expérience sur les embouteillages fantomes
    """
    M = ones((10, 10)) * 2
    M[0, 0] = Carte[0, 0]
    for j in range(1, 10):
        M[0, j] = Carte[0, j]
    for i in range(1, 10):
        M[i, 9] = Carte[0, i + 9]
    for j in range(1, 10):
        M[9, -j] = Carte[0, j + 17]
    for i in range(1, 10):
        M[-i, 0] = Carte[0, i + 26]
    return M


def compteur(Carte, voie):
    """
    prend la carte en argument et renvoie le nombre de voitures collés
    cette fonction caractérise la congestion
    """
    cpt = 0
    for i in range(0, Carte.shape[1] - 1):
        if Carte[voie, i] == 1 and Carte[voie, i + 1] == 1:
            cpt += 1
    return cpt


# Circulation

def circulation_une_voie(carte, v, voie, pro, ral):
    """
    On ajoute une voiture au début de la route avec une probabilité pro.
    Les voitures ralentissent avec une probabilité ral
    """
    assert (v > 1)
    map = carte.copy()
    n, p = map.shape
    taille_carre = 20
    init()
    fenetre = display.set_mode((p * taille_carre, n * taille_carre))
    # cet indicateur notera les coordonnées d'une voiture qui était à l'arret. Si la voiture i est dans cette liste, alors elle redémarera avec une vitesse de int(v/2). Cela permet de simuler l'accélération d'une voiture qui était arrêté.
    indRal = []
    Running = True

    while Running:
        N = nombre_de_voiture(map, voie)
        for i in range(1, N + 1):
            pral = random()
            coordonné_voiture_i = (voie, position_voiture(i, voie, map))
            if pral > ral:  # cas où la voiture ne ralentis pas
                if fin_dela_route(i, v, map, voie):
                    map[voie, position_voiture(i, voie, map)] = 0
                else:
                    if peut_avancer(i, int(v / 2), voie, map) and coordonné_voiture_i in indRal:
                        avancer(i, int(v / 2), voie, map)
                        indRal.remove(coordonné_voiture_i)
                    elif peut_avancer(i, v, voie, map):
                        avancer(i, v, voie, map)

                    elif not (peut_avancer(i, v, voie, map)):
                        dist = distance_v(i, map, voie)
                        if dist == 1:
                            avancer(i, 1, voie, map)
                        else:
                            avancer(i, v - dist, voie, map)

            else:  # cas où la voiture ralentis
                if fin_dela_route(i, v, map, voie):
                    map[voie, position_voiture(i, voie, map)] = 0
                else:
                    if peut_avancer(i, v, voie, map) and coordonné_voiture_i in indRal:
                        avancer(i, v - 1, voie, map)
                        indRal.remove(coordonné_voiture_i)
                    elif peut_avancer(i, v, voie, map):
                        avancer(i, v - 1, voie, map)
            if (voie, position_voiture(i, voie,
                                       map)) == coordonné_voiture_i:  # Dans ce cas, la voiture n'a pas avancé, on ajoute ses coordonnées à indRal et au tour suivant, elle avancera de int(v/2) si elle le peut.
                indRal.append(coordonné_voiture_i)
        pi = random()
        if pi < pro and map[voie, v] != 1:
            ajouterunevoiture(map, voie)

        fond = afficher(map)
        fenetre.blit(fond, (0, 0))
        display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                Running = False
        sleep(0.35)
    quit()


def circulationkvoie(carte, v, ListeVoie, pro_ral, p_chgt_voie):
    pro = pro_ral
    map = carte.copy()
    running = True
    indRal = []
    n, p = map.shape
    taille_carre = 10
    init()
    fenetre = display.set_mode((p * taille_carre, n * taille_carre))

    while running:
        # on fait changer les voitures de voie avant de les faire avancer.
        for k in range(0, len(ListeVoie)):
            voie = ListeVoie[k]
            if nombre_de_voiture(map, voie) != 0:
                for i in range(1, nombre_de_voiture(map, voie) - 1):
                    p = random()
                    if p < p_chgt_voie:
                        p = randint(0, 1)
                        if p == 0:
                            if peut_changer_de_voie(i, v, voie, map, 'h'):
                                changer_de_voie(i, v, voie, map, 'h')
                        if p == 1:
                            if peut_changer_de_voie(i, v, voie, map, 'b'):
                                changer_de_voie(i, v, voie, map, 'b')

        # on fait ensuite avancer les voitures
        for k in range(0, len(ListeVoie)):
            voie = ListeVoie[k]
            tic_circulation_une_voie(map, v, voie, 0.8, 0, indRal)

        fond = afficher(map)

        fenetre.blit(fond, (0, 0))
        display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        sleep(1)
        ""
    quit()


def tic_circulation_une_voie(carte, v, voie, pro, ral, indRal):
    """
    Cette fonction est en faite un passage dans la boucle infini du programme circulationunevoie, il simule une unité de temps de la circulation
    """
    map = carte
    N = nombre_de_voiture(map, voie)
    for i in range(1, N + 1):
        pral = random()
        coordonné_voiture_i = (voie, position_voiture(i, voie, map))
        if pral > ral:  # cas où la voiture ne ralentis pas
            if fin_dela_route(i, v, map, voie):
                map[voie, position_voiture(i, voie, map)] = 0
            else:
                if peut_avancer(i, int(v / 2), voie, map) and coordonné_voiture_i in indRal:
                    avancer(i, int(v / 2), voie, map)
                    indRal.remove(coordonné_voiture_i)
                elif peut_avancer(i, v, voie, map):
                    avancer(i, v, voie, map)

                elif not (peut_avancer(i, v, voie, map)):
                    dist = distance_v(i, map, voie)
                    if dist == 1:
                        avancer(i, 1, voie, map)
                    else:
                        avancer(i, v - dist, voie, map)

        else:  # cas où la voiture ralentis
            if fin_dela_route(i, v, map, voie):
                map[voie, position_voiture(i, voie, map)] = 0
            else:
                if peut_avancer(i, v, voie, map) and coordonné_voiture_i in indRal:
                    avancer(i, v - 1, voie, map)
                    indRal.remove(coordonné_voiture_i)
                elif peut_avancer(i, v, voie, map):
                    avancer(i, v - 1, voie, map)
        if (voie, position_voiture(i, voie,
                                   map)) == coordonné_voiture_i:  # Dans ce cas, la voiture n'a pas avancé, on ajoute ses coordonnées à indRal et au tour suivant, elle avancera de int(v/2) si elle le peut.
            indRal.append(coordonné_voiture_i)
    pi = random()
    if pi < pro and map[voie, v] != 1:
        ajouterunevoiture(map, voie)

    return (map, indRal)


def tic_circulation_une_voie_obstacle(carte, v, voie, pro, ral, indRal):
    """
    Cette fonction est en faite un passage dans la boucle infini du programme circulationunevoie, il simule une unité de temps de la circulation
    """
    map = carte
    N = nombre_de_voiture(map, voie)
    for i in range(1, N + 1):
        pral = random()
        coordonné_voiture_i = (voie, position_voiture(i, voie, map))
        if pral > ral:  # cas où la voiture ne ralentis pas
            if fin_dela_route(i, v, map, voie):
                map[voie, position_voiture(i, voie, map)] = 0
            else:
                if peut_avancer(i, int(v / 2), voie, map) and coordonné_voiture_i in indRal:
                    avancer(i, int(v / 2), voie, map)
                    indRal.remove(coordonné_voiture_i)
                elif peut_avancer(i, v, voie, map):
                    avancer(i, v, voie, map)

                elif not (peut_avancer(i, v, voie, map)):
                    dist = distance_v(i, map, voie)
                    if dist == 1:
                        avancer(i, 1, voie, map)
                    else:
                        avancer(i, v - dist, voie, map)

        else:  # cas où la voiture ralentis
            if fin_dela_route(i, v, map, voie):
                map[voie, position_voiture(i, voie, map)] = 0
            else:
                if peut_avancer(i, v, voie, map) and coordonné_voiture_i in indRal:
                    avancer(i, v - 1, voie, map)
                    indRal.remove(coordonné_voiture_i)
                elif peut_avancer(i, v, voie, map):
                    avancer(i, v - 1, voie, map)
        if (voie, position_voiture(i, voie,
                                   map)) == coordonné_voiture_i:  # Dans ce cas, la voiture n'a pas avancé, on ajoute ses coordonnées à indRal et au tour suivant, elle avancera de int(v/2) si elle le peut.
            indRal.append(coordonné_voiture_i)
    pi = random()
    if pi < pro and map[voie, v] != 1:
        ajouterunevoiture(map, voie)

    return (map, indRal)

# Circulation boucle


def circulation_fantome(carte, v, voie, temps_arret, timing, tours):
    """
    Met en circulation plusieurs voitures sur une route formant une boucle : les voitures arrivant à la fin de la route sont placées au début de cette dernière
    temps_arret permet de créer les embouteillages fantôme en faisant s'arreter completement une voiture pendant 2 tours
    """
    assert (v > 1)
    Temps = []
    Congestion = []
    Temps_arret = []
    temps = 0
    pos_voit_arret = -1
    cpt = 0
    map = carte.copy()
    n, p = map.shape
    taille_carre = 60
    init()
    fenetre = display.set_mode((p * taille_carre, n * taille_carre))
    # cet indicateur notera les coordonnées d'une voiture qui était à l'arret. Si la voiture i est dans cette liste, alors elle redémarera avec une vitesse de int(v/2). Cela permet de simuler l'accélération d'une voiture qui était arrêté.
    indRal = []
    Running = True

    while Running:
        N = nombre_de_voiture(map, voie)
        for i in range(1, N + 1):
            pral = random()
            coordonné_voiture_i = (voie, position_voiture(i, voie, map))
            if temps == timing and i == 7:  # on voudra arreter la voiture 7 pendant 'temps_arret' tours pour créer un bouchon fantôme
                pos_voit_arret = position_voiture(i, voie, map)
            if temps >= timing and position_voiture(i, voie, map) == pos_voit_arret and cpt < temps_arret:
                cpt += 1
            else:
                if fin_dela_route(i, v, map, voie):
                    y = map.shape[1] - position_voiture(i, voie, map)
                    if i == N:
                        if 1 not in [map[voie, l] for l in range(0, v)]:
                            map[voie, position_voiture(i, voie, map)] = 0
                            map[voie, v - y] = 1
                else:
                    if peut_avancer(i, int(v / 2), voie, map) and coordonné_voiture_i in indRal:
                        avancer(i, int(v / 2), voie, map)
                        indRal.remove(coordonné_voiture_i)
                    elif peut_avancer(i, v, voie, map):
                        avancer(i, v, voie, map)

                    elif not (peut_avancer(i, v, voie, map)):
                        dist = distance_v(i, map, voie)
                        if dist == 1:
                            avancer(i, 1, voie, map)
                        else:
                            avancer(i, v - dist, voie, map)
            if (voie, position_voiture(i, voie,
                                       map)) == coordonné_voiture_i:  # Dans ce cas, la voiture n'a pas avancé, on ajoute ses coordonnées à indRal et au tour suivant, elle avancera de int(v/2) si elle le peut.
                indRal.append(coordonné_voiture_i)
        Temps.append(temps)
        Congestion.append(compteur(map, voie))
        Temps_arret.append(timing)
        fond = afficher(pliage(map))
        fenetre.blit(fond, (0, 0))
        display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                Running = False
        sleep(0.20)
        temps += 1
        if temps == tours:
            Running = False
    quit()
    return (Temps, Congestion)


def experience_fantome(ListeCarte, voie, temps_arret, v, timing, tours):
    """
    Mise en évidence de la formation d'embouteillages fantômes, 
    """
    X = []
    Y = []
    for k in range(0, len(ListeCarte)):
        Carte = ListeCarte[k]
        XY = circulation_fantome(Carte, v, voie, temps_arret, timing, tours)
        X.append(XY[0])
        Y.append(XY[1])
    for i in range(0, len(X)):
        py.plot(X[i], Y[i], label=str(nombre_de_voiture(
            ListeCarte[i], voie)) + ' ' + "voitures")
        py.legend()
    py.xlabel("Temps")
    py.ylabel("Congestion")
    py.show()


# Diagramme fondamental


def Diagramme_fondamental(carte, voie, v, ral, pro, pos_mesure_débit, nb_points_total):
    """
    Trace le diagramme fondamental du trafic routier
    """
    assert (v > 1)
    DEBIT = []
    DENSITE = []
    den = []
    temps = 0
    tours = 0
    débit = 0
    nb_pt = 0
    map = carte.copy()
    map[voie - 1, pos_mesure_débit] = 6
    map[voie + 1, pos_mesure_débit] = 6
    n, p = map.shape
    taille_carre = 60
    init()
    fenetre = display.set_mode((taille_carre, taille_carre))
    indRal = []
    Running = True
    # on veut tracer le débit (veh/h) en fonction de la densité (veh/km)
    # on augmente pro de 0.1 tous les 60 temps
    # on pose 1h = 120tours
    # on pose 1km = 30 cases
    # on prend une carte de longueur au moins 100 cases

    while Running:
        if temps == 120:
            nbr_voit = randint(0, 250)
            map = array([[2 for k in range(0, 300)],
                         [0 for k in range(0, 300)],
                         [2 for k in range(0, 300)]])
            map[voie - 1, pos_mesure_débit] = 6
            map[voie + 1, pos_mesure_débit] = 6
            for k in range(0, nbr_voit):
                pos = randint(0, 295)
                while map[voie, pos] != 0:
                    pos = randint(0, 295)
                map[voie, pos] = 1
            temps = 0

        N = nombre_de_voiture(map, voie)
        for i in range(1, N + 1):
            pral = random()
            coordonné_voiture_i = (voie, position_voiture(i, voie, map))
            if pral > ral:  # cas où la voiture ne ralentis pas
                if fin_dela_route(i, v, map, voie):
                    map[voie, position_voiture(i, voie, map)] = 0
                else:
                    if peut_avancer(i, int(v / 2), voie, map) and coordonné_voiture_i in indRal:
                        avancer(i, int(v / 2), voie, map)
                        indRal.remove(coordonné_voiture_i)
                    elif peut_avancer(i, v, voie, map):
                        avancer(i, v, voie, map)

                    elif not (peut_avancer(i, v, voie, map)):
                        dist = distance_v(i, map, voie)
                        if dist == 1:
                            avancer(i, 1, voie, map)
                        else:
                            avancer(i, v - dist, voie, map)

            else:  # cas où la voiture ralentis
                if fin_dela_route(i, v, map, voie):
                    map[voie, position_voiture(i, voie, map)] = 0
                else:
                    if peut_avancer(i, v, voie, map) and coordonné_voiture_i in indRal:
                        avancer(i, v - 1, voie, map)
                        indRal.remove(coordonné_voiture_i)
                    elif peut_avancer(i, v, voie, map):
                        avancer(i, v - 1, voie, map)
            if (voie, position_voiture(i, voie,
                                       map)) == coordonné_voiture_i:  # Dans ce cas, la voiture n'a pas avancé, on ajoute ses coordonnées à indRal et au tour suivant, elle avancera de int(v/2) si elle le peut.
                indRal.append(coordonné_voiture_i)
            if pos_mesure_débit > coordonné_voiture_i[1] and pos_mesure_débit <= position_voiture(i, voie,
                                                                                                  map):  # dans ce cas la voiture sera passé par la case où l'on mesure le débit
                débit += 1
        pi = random()
        if pi < pro and map[voie, v] != 1:
            ajouterunevoiture(map, voie)
        den.append(densite(map, voie))
        if tours == 120:
            DEBIT.append(débit)
            débit = 0
            DENSITE.append(moyenne(den))
            den = []
            tours = 0
            nb_pt += 1

        temps += 1
        tours += 1
        fond = afficher(map)
        fenetre.blit(fond, (0, 0))
        display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                Running = False
        sleep(0.01)
        if nb_pt > nb_points_total:
            Running = False
    quit()
    py.scatter(DENSITE, DEBIT)
    py.title("Diagramme fondamental du trafic ")
    py.xlabel("Densité (veh/km)")
    py.ylabel("débit (veh/h)")
    py.show()
    print("Nombre de points :", nb_pt)


def densite(carte, voie):
    """
    Renvoie la densité (veh/km)
    """
    # 1km=30 cases
    assert (position_fin_route(carte, voie) > 30)
    N = nombre_de_voiture(carte, voie)
    return ((N * 30) / position_fin_route(carte, voie))
# Affichage graphique


def afficher(M):
    """
    Cette fonction permet l'affichage graphique, à l'aide de pygame
    """
    n, p = M.shape
    taille_carre = 20  # taille en pixels d'un carré
    init()  # initialise la fenetre
    fenetre = display.set_mode((p * taille_carre, n * taille_carre))
    fond = Surface((p * taille_carre, n * taille_carre))
    fond.fill((100, 184, 255))
    for i in range(n):  # on parcours la matrice
        for j in range(p):

            if M[i, j] == 0:
                draw.rect(fond, (127, 127, 127), [
                          j * taille_carre, i * taille_carre, taille_carre, taille_carre])

            if M[i, j] == 1:
                ""
                draw.rect(fond, (0, 0, 0), [
                          j * taille_carre, i * taille_carre, taille_carre, taille_carre])
                ""
                draw.rect(fond, (255, 228, 196),
                          [j * taille_carre, i * taille_carre, taille_carre - 3, taille_carre - 3])

            if M[i, j] == 5:
                ""
                draw.rect(fond, (0, 0, 0), [
                          j * taille_carre, i * taille_carre, taille_carre, taille_carre])
                ""
                draw.rect(fond, (255, 0, 0), [
                          j * taille_carre, i * taille_carre, taille_carre - 3, taille_carre - 3])

            if M[i, j] == 4:
                ""
                draw.rect(fond, (0, 0, 0), [
                          j * taille_carre, i * taille_carre, taille_carre, taille_carre])
                ""
                draw.rect(fond, (0, 255, 0), [
                          j * taille_carre, i * taille_carre, taille_carre - 3, taille_carre - 3])

            if M[i, j] == 6:
                ""
                draw.rect(fond, (0, 0, 0), [
                          j * taille_carre, i * taille_carre, taille_carre, taille_carre])
                ""
                draw.rect(fond, (255, 255, 0), [
                          j * taille_carre, i * taille_carre, taille_carre - 3, taille_carre - 3])

    return fond


# Cartes

CarteUneVoie = array([[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                      [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]])
CarteTroisVoie = array(
    [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
     [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]])
Fantôme1 = array(
    [[0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0]])
Fantôme2 = array(
    [[0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]])
Fantôme3 = array(
    [[0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]])
Fantôme4 = array(
    [[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]])
CarteFonda = array([[2 for k in range(0, 300)],
                    [0 for k in range(0, 300)],
                    [2 for k in range(0, 300)]])
# circulation_une_voie(CarteUneVoie, 2, 1, 0.4, 0.3)
# circulationkvoie(CarteTroisVoie, 2, [1, 2, 3], 0.2, 0.2)
# Diagramme_fondamental(CarteFonda, 1, 2, 0.1, 0, 150, 100)
# experience_fantome([Fantôme1, Fantôme2, Fantôme3, Fantôme4], 0, 3, 2, 10, 40)
