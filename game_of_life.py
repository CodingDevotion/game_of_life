#################################################################
# Par Alexandre Chartrand - 20062025
#       et
# Jad Yammine - 1067212
# TP0 - Game of Life
# Ce programme simule le jeu game of life en couleur
#
#################################################################
# Mini mode d'emploi :
#   Entrer tp0[...].py 20 pour voir le resultat apres 20 iterations.
#
#   Entrer tp0[...].py  20 -couleur pour afficher le resultat avec
#    couleurs (-couleur 20 fonctionne egalement)
#
#   Entrer tp0[...].py -animation pour enter en mode animation en
#    noir et blanc.
#
#   Entrer tp0[...].py -animation -couleur ou
#    entrer tp0[...].py -couleur -animation pour entrer en mode
#    couleur et animation.
#
#   PS: Le code du main peut avoir l'air un peu long.
#   Nous avons fait le code de facon a ce que l'ordre des
#   arguments entres n'aille pas d'importance, afin de traiter
#   tous les cas possibles.
#
#################################################################

#On import copy pour pouvoir utiliser la fonction
# deepcopy, qui permet de copier un tableau
import copy

# On importe sys pour pouvoir passer un argument directement
# dans le terminal
import sys


# Ceci permet de lire le fichier rules
def read_rules():
    f = open('rules.txt', 'r')

    # On utilise readlines pour creer un tableau de strings
    # a 2 dimensions ou chaque element du tableau correspond a une
    # ligne du fichier.
    text = f.readlines()
    f.close()
    return text

# Ceci permet de lire le fichier rules
def read_config():
    f = open('config.txt', 'r')

    # On utilise readlines pour creer un tableau de strings
    # a 2 dimensions ou chaque element du tableau correspond a une
    # ligne du fichier.
    text = f.readlines()
    f.close()
    return text


# get_config prend chacune des lignes du fichier config,
# et les place dans un ordre facile a traiter
def get_config():
    text = read_config()
    config = []

    # on lit une ligne
    for i in range(0, len(text)):

        # Si on est sur la premiere ligne, on lit les
        # dimensions de la grille et on les places dans
        # les 2 premieres cases du tableau config
        if i == 0:
            size_x, size_y = text[i].split(',')
            config.append(size_x)
            config.append(size_y)
        else:

            # Sinon, on place les coordonnees des cellules initiales
            # dans le tableau config
            color, x, y = text[i].split(',')
            config.append(color)
            config.append(x)
            config.append(y)

    return config


# get_config prend chacune des 3 lignes du fichier rules,
# et les place dans un tableau facile a traiter
def get_rules():
    text = read_rules()
    # On cree un tableau a 2 dimensions. La premiere dimension
    # comporte 3 tableaux (un pour les regles des cellules rouges,
    #  un pour les regles des cellules vertes, et un dernier pour
    # les regles des cellules bleues)
    # ex : [[3,2,3],[2,1,3],[3,2,3]]
    # Ainsi, meme si les rules ne sont pas dans le bon ordre,
    # le jeu fonctionne quand meme.

    rules = [[0 for x in range(0, 3)] for y in range(0, 3)]

    for i in range(0, 3):
        if text[i][0] == 'R':
            rules[0][0] = int(text[i][2])
            rules[0][1] = int(text[i][4])
            rules[0][2] = int(text[i][6])
        elif text[i][0] == 'G':
            rules[1][0] = 'G'
            rules[1][0] = int(text[i][2])
            rules[1][1] = int(text[i][4])
            rules[1][2] = int(text[i][6])
        elif text[i][0] == 'B':
            rules[2][0] = int(text[i][2])
            rules[2][1] = int(text[i][4])
            rules[2][2] = int(text[i][6])
    return rules


# Fonction qui cree le tableau initiale (avant toute modification)
def build_initial():
    config = get_config()
    
    # On lit les dimensions de la grille et on cree une grille vide 
    # de bonnes dimensions
    grille_initiale = [['. ' for x in range(0, int(config[0]))] \
             for y in range(0, int(config[1]))]

    # On ajoute les cellules initiales dans la grille initiale
    for i in range(2, (len(config) - 2)):
        if config[i] == 'R' or config[i] == 'G' or config[i] == 'B':
            grille_initiale[int(config[i + 2])][int(config[i + 1])]\
                = config[i] + ' '

    return grille_initiale


# Classe couleur : permet de colorer le texte lorsqu'on passe
# en mode couleur.
# La classe couleur a ete concu pour etre utilisee sur un terminal
#  de font noir.
class color:
    r = '\x1b[0;31m'
    g = '\x1b[0;32m'
    b = '\x1b[0;34m'
    default = '\x1b[0m'


# Ceci est une fonction qui convertit un tableau de donnees en une 
# suite de caracteres (string).
def convert_to_string(*grille_initiale):
    string_grid = ''

    for i in grille_initiale:
        for x in i:
            string_grid += ''.join(map(str, x))
            string_grid += '\n'
    return string_grid


# Fonction qui affiche le tableau de donnees, et qui ajoute les
# couleurs si desirees
def grid_print(couleur, string_grid):
    
    # Si la couleur n'est pas activee, on affiche 
    # la grille sans couleur
    if not couleur:
        print(string_grid)

    # Si la couleur est activee, on remplace les R par des # colores
    # en rouge, les G par des # colores en vert et les B par des #
    # colores en bleu. On affiche ensuite cette grille coloree.
    else:
        string_grid = string_grid.replace('R', color.r + '#' + color.default)
        string_grid = string_grid.replace('G', color.g + '#' + color.default)
        string_grid = string_grid.replace('B', color.b + '#' + color.default)
        print(string_grid)


# Fonction qui trouve le nombre de voisins d'une certaine case du tableau
def neighbor_finder(i, j, *grille_initiale):
    config = get_config()
    n = 0

    for g in grille_initiale:
        for h in g:

            # on verifi qu il n est pas sur le bord a droite
            if i + 1 < int(config[0]) - 1:

                # on verifi si le voisin a droite est vivant
                if h[i + 1][j] != '. ':
                    n += 1

            # on verifi qu il n'est pas sur le bord en bas
            if j + 1 < int(config[1]) - 1:

                # on verifi si le voisin en bas de lui est vivant
                if h[i][j + 1] != '. ':
                    n += 1

            # on verifi qu il n'est pas sur le bord en haut
            if j > 0:

                # on verifi si le voisin en haut est vivant
                if h[i][j - 1] != '. ':
                    n += 1

            # on verifi qu il n'est pas sur le bord en gauche
            if i > 0:

                # on verifi si le voisin a gauche est vivant
                if h[i - 1][j] != '. ':
                    n += 1

            # on verifi qu il n'est pas coin enbas a droite
            if (i + 1 < int(config[0]) - 1) and (j + 1 < int(config[1]) - 1):

                # on verifi si le voisin a droite enbas est vivant
                if h[i + 1][j + 1] != '. ':
                    n += 1

            # on verifi qu il n'est pas coin en haut a droite
            if (i + 1 < int(config[0]) - 1) and (j > 0):

                # on verifi si le voisin a droite en haut est vivant
                if h[i + 1][j - 1] != '. ':
                    n += 1

            # on verifi qu il n'est pas coin enbas a gauche
            if (j + 1 < int(config[1]) - 1) and (i > 0):

                # on verifi si le voisin a gauche enbas est vivant
                if h[i - 1][j + 1] != '. ':
                    n += 1

            # on verifi qu il n'est pas coin en haut a gauche
            if (i > 0) and (j > 0):

                # on verifi si le voisin a gauche en haut est vivant
                if h[i - 1][j - 1] != '. ':
                    n += 1
    return n


#Fonction qui update une grille avec des nouvelles cellules
def update_grid(*currentGrid):

    config = get_config()
    n = 0
    rules = get_rules()

    for h in currentGrid:

        # On cree une nouvelle grille, qui est une copie de la
        # grille actuelle.
        new = copy.deepcopy(h)

        for i in range(0, int(config[0])):

            for j in range(0, int(config[1])):

                # Regarde le nombre de voisins de chaque cellule
                # et selon les regles du jeu, on fait naitre et
                # et mourir des cellules dans la nouvelle grille.
                n = neighbor_finder(i, j, currentGrid)

                #si une cellulule est vivante, on verifie si elle
                #  meurt
                if h[i][j] != '. ':
                    if h[i][j] == 'R ':
                        if n > rules[0][2] or n < rules[0][1]:
                            new[i][j] = '. '
                    if h[i][j] == 'G ':
                        if n > rules[1][2] or n < rules[1][1]:
                            new[i][j] = '. '
                    if h[i][j] == 'B ':
                        if n > rules[2][2] or n < rules[2][1]:
                            new[i][j] = '. '

                else:
                    # Si le point est mort, on verifie si
                    # une cellule nait.
                    if n == rules[0][0]:
                        new[i][j] = 'R '
                    elif n == rules[1][0]:
                        new[i][j] = 'G '
                    elif n == rules[2][0]:
                        new[i][j] = 'B '

    # La grille actuelle devient new. Nous avons donc update la grille
    # avec des nouvelles cellules
    currentGrid = new
    return currentGrid


# Fonction qui verifie si une certaine entree x est un nombre
def is_nb(x):
    try:
        int(x)
        return True

    except ValueError:
        return False


def main():
    # User_command est un tableau qui contiendra les arguments
    # tappes par l'utilisateur
    user_command = []
    index_argument = 0
    estunNB = False

    # On stoque tous les arguments entres par l'utilisateur
    #  dans un tableau
    for arg in sys.argv:
        user_command.append(arg)

    # On commence par construire le tableau initiale avec
    # les donnees present dans config.txt
    # On initialise couleur et animation a False par defaut
    current = build_initial()
    couleur = False
    animation = False

    for z in range(len(user_command)):

        # Activation du mode couleur
        # Si l'utilisateur tape -couleur, on initialise couleur a true
        if user_command[z] == '-couleur':
            couleur = True

            # Si l'utilisateur entre un nombre, ceci veut dire que
            #  l'utilisateur a entre un nombre de frames, on fait
            # update le tableau user_commands fois et on affiche le
            #  tableau a la derniere frame calculee.
        if is_nb(user_command[z]):
            index_argument = z
            estunNB = True


        #Activation du mode animation
        # Si l'utilisateur entre animation, on affiche les cellules,
        # et on demande a l'utilisateur d'appuyer sur enter pour
        # afficher les prochaines frames.
        if user_command[z] == '-animation':

            animation = True

    # On verifie qu'on a pas entrer un nombre et -animation en meme
    #  temps
    if (animation or estunNB) and animation != estunNB:
        if animation:

            grid_print(couleur, convert_to_string(current))
            print("Voici, ci-haut, la position des cellules initiale")

            while animation:
                # Des que l"utilisateur entre un caractere quelconque
                # et qu'il appuie sur enter, animation devient false
                # et le mode animation s'arrete si on entre une
                # autre valeur


                enter = input("Appuyer sur enter pour afficher " \
                                + "la prochaine simulation" )

                if enter != '':
                    animation = False

                current = update_grid(current)
                grid_print(couleur, convert_to_string(current))

        elif estunNB:

            # On verifie que le nombre entre n'est pas negatif
            if int(user_command[index_argument]) >= 0:
                for i in range(int(user_command[index_argument])):
                    current = update_grid(current)
                grid_print(couleur, convert_to_string(current))
            else:
                # Si le nombre entre est negatif ca termine le jeux
                print('Nombre entre est negatif, simulation terminee')
        else:
            # Si on entre ni un nombre ni -animation, le jeux se termine
            print("ENTREE INCORRECT")
    else:
        # Si on entre un nombre et -animation le jeux se termine
        print('ENTREE INCORRECT')

#Lancement du main
if __name__ == "__main__":

    print('\x1b[6;30;42m' + 'Game of Life, par Alexandre Chartrand ' \
        + 'et Jad Yammine' + '\x1b[0m')
    try :
        main()

    # Si l'utilisateur appuie sur CTRL+C, on ferme le jeu
    #  sans generer d'erreurs
    except(KeyboardInterrupt):
        print('\x1b[6;30;42m' + 'Merci d\'avoir joue a Game of Life' \
              + '\x1b[0m')
