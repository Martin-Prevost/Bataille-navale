# Bataille-navale


## Liste des fonctionnalités :


**Phase 1/2 : placement des bateaux par le joueur et le robot**

Le joueur peut placer ses bâtiments uniquement sur sa grille, sans chevauchement.

Vérification que le placement des bateaux est autorisé (= les bâtiments ne se touchent pas).

L’ordinateur place ses bâtiments sans chevauchement de manière totalement aléatoire.

L’ordinateur place ses bateaux sans qu’ils se touchent (placementsdes bateaux sont autorisés).


**Interface graphique**

Interfaces Graphiques PySimpleGui :

\1) Menu de démarrage (image avec bouton play)

\2) Fenêtre de jeux :

    a) Grille du joueur

    b) Boutons de commencement et arrêt

    c) Boutons de réponses pour le joueur (apparait après le placement des bateaux)

    d) Boutons de commencement et arrêt

    e) Indication des choses à faire / case choisie par le robot / Message en cas de triche….

    f) Indication de qui doit tirer par une flamme rouge

\3) Fenêtre en cas de défaite

\4) Fenêtre en cas de victoire, on entre notre nom si on existe déjà affiche score de la partie et score total sinon affiche le score de la partie et le pseudo

\5) Fenêtre affichant les 20 premiers dans l’ordre décroissant


**Phase 3 : Jeu / Gestion des tours**

L’humain appuie sur la case a viser, le robot lui répond s’il a raté touché ou couler (si il coule, le robot dit quel bateau a été coulé), un pion rouge est placé si il touche ou coule sinon un pion bleu est placé.

L’humain peut tirer uniquement sur les cases valables de la grille du robot (un appui sur les boutons de réponses ne fait rien).

Si l’humain tape 2 fois la même case il perd un point et c’est au robot de jouer, le pion rouge déjà présent ne change pas.

Après un tir dans l’eau, le changement de joueur est automatique.

Après un tir touché (ou coulé), le même joueur garde la main.

Tour ordinateur : l’ordinateur annonce les coordonnées de son tir, le joueur lui répond s’il a touché coulé ou raté, puis l’humain place le pion du robot.


**Anti-triche :**

\1) L’ordinateur vérifie que le joueur a bien répondu, en cas de triche : tour annulé, bip sonore, -10 points, le robot rejoue.

\2) L’ordinateur vérifie que le joueur a bien placé le pion sur la case demandée, en cas de triche : tour annulé, bip sonore, -10 points, le robot rejoue. (si le joueur appuie de nouveau sur un bouton de réponse on considère que le joueur a mal placé le pion).

**Stratégie de tir du robot (tir intelligent)**
**Fonctionnalité commune pour les 2 modes de tirs :**

\1) Le robot ne tire jamais 2 fois la même case

\2) Le robot ne tire pas sur les cases juxtaposées aux bateaux déjà coulés

\3) Le robot ne tire que des cases valides (de A à J et de 1 à 10 = prise en compte des bateaux au bord du damier).

Le tire intelligent est constitué de 2 modes, un mode de recherche et un mode qui s’active lorsque le robot touche un bateau.

**Mode 1 :** c’est le mode que le robot commence à utiliser jusqu’à toucher un bateau. Il s’active lorsque qu’un bateau est coulé jusqu’à toucher un bateau. Il consiste à chercher un nouveau bateau, il tire uniquement sur les diagonales 1 sur 2 (ex : échecs : tire uniquement sur les cases noires) cela divise le nombre de cases par 2, et augmente l’espérance de toucher un bateau.

**Mode 2 :** il s’active dès qu’un bateau est touché et s’arrête lorsque le bateau est coulé. Il commence par taper aléatoirement les 4 cases juxtaposées à la case touchée (parmi les 4 cases uniquement les cases valides : dans la grille et pas déjà tirées) Dès qu’il touche une deuxième case, il tapera uniquement aléatoirement les 2 cases possibles : juxtaposées et alignées au 2 cases précédentes (parmi les 2 cases uniquement les cases valides = dans la grille et pas déjà tirées) Il répète la dernière opération jusqu’à couler le bateau puis on repasse sur le mode 1 de tir.

**Gestion des scores**

En début de partie chaque joueur a 25 points

Chaque tir coûte 1 point

Chaque ”touché” rapporte 1 point. Chaque ”coulé” rapporte 2 points par case du bâtiment coulé (exemple : couler le croiseur rapporte au total : 1x4 (lors des touchés successifs) + 2x4 (une fois coulé) = 12). Il faudra enlever les points perdus lors de chaque tir.

Si un joueur n’a plus de points il ne peut plus tirer : la partie s’arrête et l’adversaire est désigné gagnant. (Points négatifs impossibles)

Si un joueur coule tous les bateaux adverses, la partie s’arrête et ce joueur est désigné gagnant.

Si le joueur humain triche, il perd 10 points.

Si le gagnant est le joueur humain, il donne un pseudo. Le score du  gagnant est enregistré et affiché. Si le gagnant existait déjà dans la liste des scores, les points sont cumulés et affichés.

Prise en compte s’il y a des majuscules ou non on ne fait pas la différence. Prise en compte des noms composés, des espaces…

Ensuite (après fermeture de la fenêtre) on affiche dans l’ordre décroissant les 20 premiers du classement.

Les scores sont stockés dans un fichier txt dans l’ordre décroissant  avec le pseudo associé ((première ligne à ne pas prendre en compte indice de longueur))


**Effet sonore**

Différents effets sonores :

\1) Lorsqu’on rate

\2) Lorsqu’on touche

\3) Lorsqu’on coule

\4) Lorsqu’on gagne

\5) Lorsqu’on perd

\6) Lorsqu’on triche

TTS : le robot dit à voix haute la case qu’il tire

Exemple : « Je joue en A1 »
