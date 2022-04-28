"""
Création : 03/04/2021
Personnes : Martin Prévost

Bibliothèques : 
    PySimpleGUI
    random    
    pygame
"""

import PySimpleGUI as sg
from random import randint
import pygame

#----Ecran d'accueille----
pygame.init()

sg.theme('LightGrey1')
start = [[sg.B('', image_filename='menu.png', key='Start')]]
window = sg.Window('Bataille Navale', layout=start)

while True:
    event, values = window.read()
    if event == 'Start':
        break
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

window.close()

#----Phase de Jeu----
#----Phase 1 : Placement des bateaux par le joueur----

def autour_bateau(tab):
    '''
    Récupérer les cases autour d'un bateau ou autour d'un groupe de cases

    Parameters
    ----------
    tab : list
        tableau avec les vecteurs correspondant aux cases

    Returns
    -------
    autour : list
        tableau avec les cases et les cases autours

    '''
    autour = []
    for i in range(0,len(tab)):
        autour.append(tab[i])
        autour.append((tab[i][0]+1,tab[i][1]))
        autour.append((tab[i][0]-1,tab[i][1]))
        autour.append((tab[i][0],tab[i][1]+1))
        autour.append((tab[i][0],tab[i][1]-1))  
    autour = list(set(autour))          #enveler les doublets
    return autour

def verif(t1,t2):
    '''
     Vérifier qu'un bateau est bien placé par rapport aux autres

    Parameters
    ----------
    t1 : list
        cases des autres bateaux
    t2 : list
        cases d'un bateau

    Returns
    -------
    int
        indice vrai ou faux : bien placé ou non
    save : list
        tableau avec les cases fausses

    '''
    save = []
    res = False
    for i in range(len(t2)):
        if t2[i] in t1:
            save.append(t2[i])
            res = True
    autour = autour_bateau(t1)[:]
    for i in range(len(t2)):
        if t2[i] in autour:
            res = True
    return res, save

def reste(tab,save):
    '''
    Enlever un bateau mal placé

    Parameters
    ----------
    tab : list
        coordonnées des cases du tableau
    save : list
        cases déjà utilisées par un autre bateau

    Returns
    -------
    None.
    '''
    for i in range(len(tab)):
        if tab[i] not in save:
            window[tab[i]].update('', button_color=('white'))
    
def placement_j(n):
    '''
    Placement des n cases d'un bateau de manière juxtaposée

    Parameters
    ----------
    n : int
        taille du bateau

    Returns
    -------
    tab : list
        coordonnées des cases du bateau

    '''
    tab = []
    cpt = 0
    while True:
        event, values = window.read()
        if type(event)==tuple and min(event)>10:
            window[event].update('◯', button_color=('green'))
            tab.append(event)
            cpt += 1
            break
    while True:
        event, values = window.read()
        if type(event)==tuple and min(event)>10:
            if (event[0]==tab[0][0]-1 or event[0]==tab[0][0]+1) and event[1]==tab[0][1]:
                break
            if (event[1]==tab[0][1]-1 or event[1]==tab[0][1]+1) and event[0]==tab[0][0]:
                break
    cpt +=1
    window[event].update('◯', button_color=('green'))
    tab.append(event)
    save1 = [tab[0][1],tab[1][1]]
    save2 = [tab[0][0],tab[1][0]]
    if n>2:
        while True:
            event, values = window.read()
            if type(event)==tuple and min(event)>10:
                if tab[0][0]==tab[1][0] and tab[0][0]==event[0]:
                    if event[1]==min(save1)-1 or event[1]==max(save1)+1:
                        save1.append(event[1])
                        window[event].update('◯', button_color=('green'))
                        tab.append(event)
                        cpt += 1
                        if cpt==n:
                            break
                        continue
                if tab[0][1]==tab[1][1] and tab[0][1]==event[1]:
                    if event[0]==min(save2)-1 or event[0]==max(save2)+1:
                        save2.append(event[0])
                        window[event].update('◯', button_color=('green'))
                        tab.append(event)
                        cpt += 1
                        if cpt==n:
                            break
    return tab

def recur_placement(t_tot,t1,a):
    '''
     Placer le nouveau bateau jusqu'à que tout soit correct (collé/chevauchement)

    Parameters
    ----------
    t_tot : list
        coordonnées des bateaux précédents
    t1 : list
        coordonnées du nouveau bateau (à vérifier)
    a : int
        longueur du bateau

    Returns
    -------
    t1 : tab
        coordonnées du nouveau bateau
    '''
    while True:
        res, save = verif(t_tot,t1)   #on vérifie si c'est juste
        if res==False:
            return t1
        if res==True:
            reste(t1,save)           #on reset les cases du bateau
            t1 = placement_j(a)[:]   #on redemande un new bateau
         
def phase_1():
    '''
    Placer les 5 bateaux avec appel aux fonctions de placement et vérification et message d'info

    Returns
    -------
    emplacement : list
        liste des coordonnées des cases de l'emsemble des bateaux du joueur

    '''
    window['Commencer'].update(visible=False)
    window['Finir'].update(visible=False)
    
    window['faire'].update('Vous devez placer vos différents bateaux')
    window['flotte'].update('Placez votre porte-avions : 5 cases')
    tab_5 = placement_j(5)[:]
    
    window['flotte'].update('Placez votre croiseur : 4 cases')
    tab_4 = placement_j(4)[:]
    tab_save_4 = recur_placement(tab_5,tab_4,4)[:]
     
    window['flotte'].update('Placez votre contre-torpilleur n1 : 3 cases')
    tab_3_1 = placement_j(3)
    tab_tot1 = tab_5[:] + tab_save_4[:]
    tab_save_3_1 = recur_placement(tab_tot1,tab_3_1,3)[:]
    
    window['flotte'].update('Placez votre contre-torpilleur n2: 3 cases')
    tab_3_2 = placement_j(3)[:]
    tab_tot2 = tab_tot1[:] + tab_save_3_1[:]
    tab_save_3_2 = recur_placement(tab_tot2,tab_3_2,3) 
    
    window['flotte'].update('Placez votre sous-marin : 2 cases')
    tab_2 = placement_j(2)[:]
    tab_tot3 = tab_tot2[:] + tab_save_3_2[:]
    tab_save_2 = recur_placement(tab_tot3,tab_2,2)
    
    emplacement = tab_tot3[:] + tab_save_2[:]
    window['flotte'].update('')
    return emplacement

#----Phase 2 : Placement des bateaux par le robot----

def placement_bot(n):
    '''
    Placement aléatoire d'un bateau de n cases (pour le robot)

    Parameters
    ----------
    n : int
        longeur du bateau

    Returns
    -------
    bateau : list
        coordonnées des n cases du nouveau bateau 

    '''
    alea = randint(0,1)
    bateau = [(0, 0)]*n
    if alea == 0: 
        ligne = randint(1,11-n)
        colone = randint(1,10)
        for i in range(len(bateau)):
            bateau[i] = (ligne+i,colone)            
    if alea == 1:
        ligne = randint(1,10)
        colone = randint(1,11-n)
        for i in range(len(bateau)):
            bateau[i] = (ligne,colone+i)
    return bateau    

def verif_bot(total,new):
    '''
    Vérification que le nouveau bateau est valide (pas collé à un autre bateau
    et pas de chevauchement)

    Parameters
    ----------
    total : list
        tableau contenant les anciens bateaux
    new : list
        nouveau bateau

    Returns
    -------
    res : booleen
        true valide / false invalide

    '''
    res = True
    for i in range(len(new)):
        if new[i] in total:
            res = False
    autour = autour_bateau(total)[:]
    for i in range(len(new)):
        if new[i] in autour:
            res = False
    return res

def phase_2():
    '''
    Placement par le robot des bateaux

    Returns
    -------
    coordonner_bot : list
        coordonnées des cases des différents bateaux

    '''
    coordonner_bot = placement_bot(5)     #place un bateau de taille n=5
    
    bateau_4 = placement_bot(4)
    while verif_bot(coordonner_bot,bateau_4) == False:  #s'arrete quand bateau_4 
        bateau_4 = placement_bot(4)                #n'est pas collé ou au dessus de bateau_5
    
    bateau_3_1 = placement_bot(3)
    coordonner_bot += bateau_4[:]
    while verif_bot(coordonner_bot,bateau_3_1) == False:
        bateau_3_1 = placement_bot(3)
    
    bateau_3_2 = placement_bot(3)
    coordonner_bot += bateau_3_1[:]
    while verif_bot(coordonner_bot,bateau_3_2) == False:
        bateau_3_2 = placement_bot(3)
    
    bateau_2 = placement_bot(2)
    coordonner_bot += bateau_3_2[:]
    while verif_bot(coordonner_bot,bateau_2) == False:
        bateau_2 = placement_bot(2)
        
    coordonner_bot += bateau_2  
    #décommenter pour afficher les bateaux ennemis (utile pour le debug et le dev)
    """
    for i in range(len(coordonner_bot)):
        window[coordonner_bot[i]].update(button_color=('','green'))
    """
    return coordonner_bot 

#----Phase 3 : Phase de tir----
                    
def couler_bateau(tire,coord,indice):
    '''
    Détermine si un bateau a été coulé, si oui on affiche un message et on 
    modifie la première case du bateau coulé par (0,0) dans le tableau coord 
    pour savoir lesquelles sont déjà coulées. Fonction commune au robot et au joueur.

    Parameters
    ----------
    tire : list
        Tableau contenant l'historique des tirs.
    coord : list
        coordonnées des différents bateaux.
    indice : str
        Pour le message coulé par le 'robot' ou le 'joueur'.

    Returns
    -------
    Booléen
        True : un bateau est coulé, None : l'inverse.
    coord : list
        coordonnées des différents bateaux.
    int
        score à ajouter.
    int
        indice pour le tir intelligent : savoir si dernier tir a mené à un 'coulé'.

    '''
    bateau = [0,5,9,12,15,17]
    longeur = ['porte-avions','croiseur','contre-torpilleur n1','contre-torpilleur n2'
               ,'sous-marin']
    for i in range(len(bateau)-1):
        if set(coord[bateau[i]:bateau[i+1]]).issubset(set(tire))==True:
            window['flotte'].update(str(indice)+str(longeur[i])+' !')
            coord[bateau[i]] = (0, 0)
            return True, coord, bateau[i+1]-bateau[i], 2
    return None, coord, 0, 0       
                           
def couler(tire,coord,score):
    '''
    Changer le score en cas de touché ou coulé

    Parameters
    ----------
    tire : list
        Tableau contenant l'historique des tirs.
    coord : list
        coordonnées des différents bateaux.
    score : int
        score du joueur.

    Returns
    -------
    list
        coordonnées des différents bateaux modifiés ou non.
    int
        score modifié.

    '''
    indice = 'Vous avez coulé le '
    rep, coordonner, score_add, mar = couler_bateau(tire,coord,indice)
    if rep==True:
        pygame.mixer.Sound('couler.mp3').play()
        return coordonner, score+(score_add*2)
    if tire[-1] in coord:
        window['flotte'].update('Vous avez touché un bateau !')
        return coord, score+1
  
def toucher(tire,coord):
    '''
    Savoir si le joueur a touché ou coulé ou raté et donc qui doit jouer après.

    Parameters
    ----------
    tire : list
        Tableau contenant l'historique des tirs.
    coord : list
        coordonnées des différents bateaux.
        
    Returns
    -------
    bool
        Le joueur garde la main ou c'est au robot de jouer.

    '''
    if tire[-1] in tire[0:len(tire)-1]:   #case déjà tiré 
        pygame.mixer.Sound('plouffe.mp3').play(0, 0, 5000)
        return False
    if tire[-1] in coord:
        window[tire[-1]].update('⬤', button_color=('red',''))
        explosion_son = pygame.mixer.Sound("explosion.ogg")
        explosion_son.play()
        return True
    else:
        pygame.mixer.Sound('plouffe.mp3').play(0, 0, 5000)
        window[tire[-1]].update('⬤', button_color=('#5DADE2',''))
        window['flotte'].update('Raté')
        return False

def tire_joueur(tire_du_joueur,n):   
    '''
    Demander au joueur de tirer, et ajouter la case à l'historique de tirs

    Parameters
    ----------
    tire_du_joueur : list
        Tableau contenant l'historique des tirs.
    n : booléen
        indice : déjà tiré ou pas : utile pour le 'message'

    Returns
    -------
    tire_du_joueur : list
        Tableau contenant l'historique des tirs et la nouvelle case.

    '''
    while True:
        if n==False:
            window['faire'].update('Sélectionnez une case à torpiller')
        if n==True:
            window['faire'].update('Sélectionnez une nouvelle case à torpiller')
        event, values = window.read()
        if type(event)==tuple and max(event)<11:
            tire_du_joueur.append(event)
            break
    return tire_du_joueur

def alea_tire_bot(tire_b):
    '''
    Tire intélligent : Mode 1 : tire une case aléatoire pas déjà touchée 
    (et pas à coté des bateaux coulés) et uniqement sur les diagonales une sur deux.

    Parameters
    ----------
    tire_b : list
        Tableau contenant l'historique des tirs et les cases 'interdites'.

    Returns
    -------
    tire_b : list
        Tableau contenant l'historique des tirs et la nouvelle case.

    '''
    ligne = randint(11,20)        
    col = randint(1,5)*2+10 
    if (ligne % 2) == 0:
        col-=1
    while ((ligne, col) in tire_b)==True:
        ligne = randint(11,20)        
        col = randint(1,5)*2+10 
        if (ligne % 2) == 0:
            col-=1
    tire_b.append((ligne, col))
    return tire_b

def chasse(tire_b,save_case): 
    '''
    Tir intélligent : Mode 2.1 : après avoir touché  une case on en cherche une
    juxtaposée jusqu'à toucher ou couler

    Parameters
    ----------
    tire_b : list
        Tableau contenant l'historique des tirs.
    save_case : list
        case touchée du bateau chassé.

    Returns
    -------
    tire_b : list
        Tableau contenant l'historique des tirs et la nouvelle case.

    '''
    new_tire = (1,50)
    while (min(new_tire) > 10 and max(new_tire) < 21 and (new_tire not in tire_b))==False:
        alea = randint(1,4)
        if alea == 1 :
            new_tire = (save_case[0][0]-1,save_case[0][1])
        if alea == 2 :
            new_tire = (save_case[0][0]+1,save_case[0][1])
        if alea == 3 :
            new_tire = (save_case[0][0],save_case[0][1]-1)
        if alea == 4 :
            new_tire = (save_case[0][0],save_case[0][1]+1)
    tire_b.append(new_tire)
    return tire_b
  
def chasse1(tire_b,save_case):  
    '''
    Tir intélligent : Mode 2.2 : après avoir touché 2 cases d'un même bateau, 
    on tire aléatoirement sur les 2 cases possibles (si elles sont valides)

    Parameters
    ----------
    tire_b : list
        Tableau contenant l'historique des tirs.
    save_case : list
        cases touchées du bateau chassé.

    Returns
    -------
    tire_b : list
        Tableau contenant l'historique des tirs et la nouvelle case.

    '''
    new_tire = (1,50)
    while (min(new_tire) > 10 and max(new_tire) < 21 and (new_tire not in tire_b))==False:
        alea = randint(1,2)
        if save_case[0][0]==save_case[1][0]:            
            if alea==1:
                mini_tab=save_case[0][1]
                for i in range(len(save_case)):
                    if mini_tab>save_case[i][1]:
                        mini_tab=save_case[i][1]
                new_tire = (save_case[0][0],mini_tab-1,)           
            if alea==2:
                max_tab=save_case[0][1]
                for i in range(len(save_case)):
                    if max_tab<save_case[i][1]:
                        max_tab=save_case[i][1]
                new_tire = (save_case[0][0],max_tab+1)
               
        if save_case[0][1]==save_case[1][1]:           
            if alea==1:
                mini_tab=save_case[0][0]
                for i in range(len(save_case)):
                    if mini_tab>save_case[i][0]:
                        mini_tab=save_case[i][0]
                new_tire = (mini_tab-1,save_case[0][1])         
            if alea==2:
                max_tab=save_case[0][0]
                for i in range(len(save_case)):
                    if max_tab<save_case[i][0]:
                        max_tab=save_case[i][0]
                new_tire = (max_tab+1,save_case[0][1])
    tire_b.append(new_tire)
    return tire_b
        
def tire_bot(tire_b,etat,save_case,nb_touche):
    '''
    Tir du robot : Choisie entre le mode de tir 1 ; 2.1 et 2.2 
    elle peut initialiser le tableau save_c qui stocke les cases du bateau chassé
    
    Parameters
    ----------
    tire_b : list
        Tableau contenant l'historique des tirs.
    etat : int
        indice pour choisir le mode de tir provenant entre autre de la réponse du joueur.
    save_case : list
        cases touchées du bateau chassé.
    nb_touche : int
        nombre de cases touchées par le robot sur le bateau chassé.

    Returns
    -------
    tire_b : list
        Tableau contenant l'historique des tirs et la nouvelle case.
    save_case : list
        cases touchées du bateau chassé.

    '''
    if etat==0 or etat==2:
        if len(save_case)>1:
            save_c = autour_bateau(save_case)
            tire_b = tire_b[:] + save_c[:]
            save_case = []
        tire_b = alea_tire_bot(tire_b)[:]
    if etat==1:
        if nb_touche==1:
            save_case = []
            save_case.append(tire_b[-1])
            tire_b = chasse(tire_b,save_case)[:]
        if nb_touche==2:
            tire_b = chasse(tire_b,save_case)[:]
        if nb_touche>2:
            tire_b = chasse1(tire_b,save_case)[:]           
    alpha = '-ABCDEFGHIJ'
    localisation = 'Je joue en : '+str(alpha[tire_b[-1][1]-10])+str(tire_b[-1][0]-10)
    window['bot'].update(localisation)
    pygame.mixer.Sound("audio/"+str(alpha[tire_b[-1][1]-10])+str(tire_b[-1][0]-10)+'.mp3').play()
    return tire_b, save_case

def placement_pion_bot(coord,tire,score,etat,nb_touche,save_case):
    '''
    Réponse du joueur au robot et placement du pion par le joueur; anti triche et reste de 
    tour; appel aux fonctions pour calculer le score, savoir si un bateau est coulé..; 
    changement des indices pour le tir intélligent; jouer les effets sonores;
    message d'indication pour le joueur; sauvegarde dans save_case de la case si touchée ou 
    coulée.
    
    Parameters
    ----------
    coord : list
        coordonnées des bateaux du robot.
    tire : list
        Tableau contenant l'historique des tirs.
    score : int
        score du joueur.
    etat : int
        indice pour le choisir le mode de tir intélligent.
    nb_touche : int
        indice du nb de cases touchées d'un même bateau.
    save_case : list
        cases touchées du bateau chassé.

    Returns
    -------
    list
        coordonnées des bateaux du robot (modifier si un bateau est coulé).
    bool
        qui joue : robot ou joueur.
    int
        score du joueur.
    int
        score à enlever si triche.
    tire : list
        Tableau contenant l'historique des tirs et la nouvelle case.
    int
        etat : indice pour le choisir le mode de tir intélligent.
    nb_touche : int
        indice du nb de cases touché d'un même bateau..
    save_case : list
        cases touchées du bateau chassé + eventuellement une nouvelle.

    '''
    new_tire = []
    save_score = score
    save_coord = coord[:]
    for i in range(len(tire)):
        new_tire.append((tire[i][0],tire[i][1]))
    while True:
        window['faire'].update('Répondez au robot si il a raté ou touché ou coulé')
        event, values = window.read()
        if event == 'Touché' or event == 'Coulé' or event == 'Raté':          
            if new_tire[-1] not in coord:
                window['flotte'].update('Le robot a raté')
                a = False
                if event != 'Raté':
                    pygame.mixer.Sound("cheat.mp3").play()
                    window['info'].update('Vous avez triché sur la réponse !!!')
                    window['flotte'].update('Le tour est annulé')
                    del tire[-1]
                    return save_coord, True, save_score+1, -10, tire, etat, nb_touche, save_case               
            indice = 'Le robot a coulé le '
            bool1, coord, add_scores, etat2 = couler_bateau(new_tire,coord,indice) 
            score += add_scores*2
            if bool1 == True: 
                a = True
                if event != 'Coulé':
                    pygame.mixer.Sound("cheat.mp3").play()                   
                    window['info'].update('Vous avez triché sur la réponse !!!')
                    window['flotte'].update('Le tour est annulé')
                    del tire[-1]
                    return save_coord, True, save_score+1, -10, tire, etat, nb_touche, save_case           
            if bool1 == None:           
                if new_tire[-1] in coord:    
                    window['flotte'].update('Le robot a touché un bateau')
                    score += 1
                    a = True
                    if event != 'Touché':
                        pygame.mixer.Sound("cheat.mp3").play()                    
                        window['info'].update('Vous avez triché sur la réponse !!!')
                        window['flotte'].update('Le tour est annulé')
                        del tire[-1]
                        return save_coord, True, save_score+1, -10, tire, etat, nb_touche, save_case
            
            window['faire'].update('Placer la case du robot demandée')
            event, values = window.read()
            chang = (tire[-1][0],tire[-1][1])
            if event != chang:
                pygame.mixer.Sound("cheat.mp3").play()             
                window['info'].update('Vous avez triché sur la localisation !!!')
                window['flotte'].update('Le tour est annulé')
                del tire[-1]
                return save_coord, True, save_score+1, -10, tire, etat, nb_touche, save_case          
            if a==False:
                window['info'].update('')
                window[chang].update('⬤', button_color=('#5DADE2',''))
                if etat==1 and len(save_case)==1:
                    nb_touche=2
                if etat==1 and len(save_case)>1:
                    nb_touche=3
                pygame.mixer.Sound('plouffe.mp3').play(0, 0, 5000)
                return coord, False, score, 0, tire, etat, nb_touche, save_case
            if a==True:
                window['info'].update('')
                window[chang].update('⬤', button_color=('red',''))
                if etat2==0:
                    pygame.mixer.Sound("explosion.ogg").play()
                    if etat==1:
                        nb_touche = 3
                    if etat==0:
                        nb_touche = 1
                    etat2=1
                    save_case.append(tire[-1])
                if etat2==2:
                    pygame.mixer.Sound('couler.mp3').play()                   
                    nb_touche = 0
                    etat2 = 0
                    save_case.append(tire[-1])
                return coord, True, score, 0, tire, etat2, nb_touche, save_case

def stop_jeu(coord_joueur,coord_bot):
    '''
    Arrêter la partie si plus de points ou tous les bateaux sont coulés

    Parameters
    ----------
    coord_joueur : list
        Coordonnées des bateaux du joueur.
    coord_bot : list
        Coordonnées des bateaux du robot.

    Returns
    -------
    bool
        Si partie finie = True sinon false.

    '''
    if coord_joueur[0] == (0, 0) and coord_joueur[5] == (0, 0) and coord_joueur[9] == (0, 0) and coord_joueur[12] == (0, 0) and coord_joueur[15] == (0, 0):
        return True
    if coord_bot[0] == (0, 0) and coord_bot[5] == (0, 0) and coord_bot[9] == (0, 0) and coord_bot[12] == (0, 0) and coord_bot[15] == (0, 0):
        return True
    return False 

def phase_3(coord_joueur,coord_bot):
    '''
    Gére qui doit tirer et fait appel au différentes fonctions de tir...
    Renvoie le score final en fin de partie

    Parameters
    ----------
    coord_joueur : list
        Coordonnées des bateaux du joueur.
    coord_bot : list
        Coordonnées des bateaux du robot.

    Returns
    -------
    score_bot : int
        score du robot.
    score_joueur : int
        score du joueur.

    '''
    window['Raté'].update(visible=True)
    window['Touché'].update(visible=True)
    window['Coulé'].update(visible=True)
    score_bot = 25
    score_joueur = 25
    tire_du_joueur = []
    tire_du_bot = []
    etat = 0
    save_case = []
    nb_touche = 0   
    window['t_joueur'].update(image_filename='fire.png')
    while score_bot>0 and score_joueur>0:
        n=False
        tire_du_joueur = tire_joueur(tire_du_joueur,n)
        score_joueur -= 1
        while toucher(tire_du_joueur,coord_bot)==True:
            coord_bot, score_joueur = couler(tire_du_joueur,coord_bot,score_joueur)
            if stop_jeu(coord_joueur,coord_bot) == True:
                break
            if score_bot<1 or score_joueur<1:
                break
            n=True
            tire_du_joueur = tire_joueur(tire_du_joueur,n)
            score_joueur -= 1
        if stop_jeu(coord_joueur,coord_bot) == True:
            break       
        reponce = True 
        window['t_joueur'].update(image_filename='blanc.png')
        window['t_bot'].update(image_filename='fire.png')
        while reponce == True:
            if stop_jeu(coord_joueur,coord_bot) == True:
                break
            if score_bot<1 or score_joueur<1:
                break
            tire_du_bot, save_case = tire_bot(tire_du_bot,etat,save_case,nb_touche) 
            score_bot -= 1
            coord_joueur, reponce, score_bot, add_score_j, tire_du_bot, etat, nb_touche, save_case = placement_pion_bot(coord_joueur,tire_du_bot,score_bot,etat,nb_touche,save_case)
            score_joueur += add_score_j

        window['t_joueur'].update(image_filename='fire.png')
        window['t_bot'].update(image_filename='blanc.png')
        if stop_jeu(coord_joueur,coord_bot) == True:
            break        
    return score_bot, score_joueur  

#----Affichage graphique---

score_bot = 'stop'
score_joueur = 'stop' 
alphab = 'ABCDEFGHIJ'
nb_col = nb_ligne = 10

layout_bot = [[sg.T('', key=('bot'), size=(50, 3))]]
layout_bot += [[sg.Button('', size=(4,2), pad=(0,0), button_color=('white'), key=('t_bot'))]+
               [sg.Button(alphab[i], pad=(0,0), size=(4,2), key=('rien1'), button_color=('#318CE7')) 
                for i in range(nb_col)]]
layout_bot += [[sg.B(i, size=(4,2), pad=(0,0), button_color=('#318CE7'))]+
               [sg.Button('', size=(4, 2), key=(i,j), pad=(0,0), button_color=('white')) 
                for j in range(1,1+nb_col)] for i in range(1,1+nb_col)]

layout_j = [[sg.T('', key=('flotte'), size=(50, 3))]]
layout_j += [[sg.Button('', size=(4,2), pad=(0,0), button_color=('white'), key=('t_joueur'))]+
             [sg.Button(alphab[i], pad=(0,0), size=(4,2), key=('rien2'), button_color=('#318CE7')) 
              for i in range(nb_col)]]
layout_j += [[sg.B(i-10, size=(4,2), pad=(0,0), button_color=('#318CE7'))]+
             [sg.Button('', size=(4, 2), key=(i,j), pad=(0,0), button_color=('white')) 
              for j in range(nb_col+1,nb_col+11)] for i in range(nb_ligne+1,nb_ligne+11)]

lay_button = [[sg.Button("Raté", visible=False, pad=(0,0))]]
lay_b2 = [[sg.Button("Touché", visible=False, pad=(0,0))]]
lay_b3 = [[sg.Button("Coulé", visible=False, pad=(0,0))]]

lay_button2 = [[sg.T('', key=('info'), size=(30, 1))]]
lay_button2 += [[sg.T('Chose à faire :'), 
                 sg.T('Appuyez sur commencer pour débuter', key=('faire'), size=(25, 2))]]
lay_button3 = [[sg.Button("Commencer"), sg.Button("Finir")]]

layout_var = [[sg.Frame('Ennemi', layout_bot, title_color='red', pad=(10,10))]+
              [sg.Frame('Vous', layout_j, title_color='blue')],
              [sg.Column(lay_button, justification='centrer')]+
              [sg.Column(lay_b2, justification='centrer')]+
              [sg.Column(lay_b3, justification='centrer')],
              [sg.Column(lay_button2, justification='centrer')],
              [sg.Column(lay_button3, justification='centrer')]]

window = sg.Window('Bataille navale', layout=layout_var)   #afficher la fenêtre

#----Boucle while : appel des phases 1,2 et 3----

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Finir':
        break
    if event == 'Commencer':
        coord_joueur = phase_1()[:]   #phase de placement des bateaux par le joueur
        coord_bot = phase_2()[:]      #phase de placement des bateaux du bot
        score_bot, score_joueur = phase_3(coord_joueur,coord_bot)  #phase de tir
        break
        
window.close()

#----Partie finie : gestion de la base de données et score----

def changement_ordre(nom, score):
    '''
    Trie les scores avec les pseudos associés dans l'ordre décroissant.

    Parameters
    ----------
    nom : list
        liste des pseudos.
    score : list
        liste des scores.

    Returns
    -------
    nom : list
        liste des pseudos triés.
    score : list
        liste des scores triés.

    '''
    n = len(nom)
    for i in range(n):
        for j in range(0, n-i-1):
            score_nb1 = int(score[j][0:score[j].find('!')])
            score_nb2 = int(score[j+1][0:score[j+1].find('!')])
            if score_nb1 < score_nb2:
                score[j], score[j+1] = score[j+1], score[j]
                nom[j], nom[j+1] = nom[j+1], nom[j]
    return nom, score  

def remplisage_actu(nom, score):
    '''
    Réécrire le fichier txt trié

    Parameters
    ----------
    nom : list
        liste des pseudos.
    score : list
        liste des scores.

    Returns
    -------
    data_base : list
        contient tous les pseudos et scores associés pour afficher la base de données.

    '''
    f = open("score_data.txt", "w", encoding="utf8")
    f.write(str(2*len(nom))+'!\n')
    data_base = []
    for j in range(len(nom)):
        f.write(str(nom[j][0:nom[j].find('!')]).upper()+'!\n')
        f.write(str(score[j][0:score[j].find('!')])+'!\n')
        data_base.append(str(nom[j][0:nom[j].find('!')])+' : '+
                         str(score[j][0:score[j].find('!')]))
    f.close()  
    return data_base

def cherche_pseudo(nom,score,pseudo,score_joueur):
    '''
    Si le joueur existe : afficher le score total sinon add le joueur dans base 
    de données fait appel aux fonctions changement_ordre et remplisage_actu

    Parameters
    ----------
    nom : list
        liste des pseudos.
    score : list
        liste des scores.
    pseudo : str
        Pseudo du joueur.
    score_joueur : int
        score du joueur.

    Returns
    -------
    data_base : list
        contient tous les pseudos et scores associés pour afficher la base de données.

    '''
    for i in range(len(nom)):
        if pseudo.upper() == str(nom[i][0:nom[i].find('!')]):
            score[i] = int(score[i][0:score[i].find('!')]) + score_joueur          
            affichage = 'Pseudo : '+str(nom[i][0:nom[i].find('!')].lower())+'\n'
            window['res'].update(affichage+'Vous avez un score total : '+str(score[i]))  
            score[i] = str(score[i])+'!'
            nom_new, score_new = changement_ordre(nom, score)[:]
            data_base = remplisage_actu(nom_new, score_new)
            return data_base
    nom.append(pseudo)          
    score.append(score_joueur)
    affichage = 'Nouveau joueur : '+str(nom[-1])+'\n'+'Vous avez '+str(score[-1])+' de score !'
    window['res'].update(affichage)
    nom[-1] = str(nom[-1])+'!'
    score[-1] = str(score[-1])+'!'
    nom_new, score_new = changement_ordre(nom, score)[:]
    data_base = remplisage_actu(nom_new, score_new)    
    return data_base
     
def resultat(pseudo,score_joueur):
    '''
    Lis le fichier score_data.txt pour crée 2 tableaux : nom et score

    Parameters
    ----------
    pseudo : str
        Pseudo du joueur.
    score_joueur : int
        score du joueur.

    Returns
    -------
    data_base : list
        contient tous les pseudos et scores associés pour afficher la base de données.

    '''
    f = open("score_data.txt", "r", encoding="utf8")
    nom = []
    score = []
    longeur = f.readline()
    longeur = longeur[0:longeur.find('!')]
    for i in range(int(longeur)):
        if (i % 2) == 0:
            nom.append(f.readline())
        else:
            score.append(f.readline())
    f.close()
    data_base = cherche_pseudo(nom,score,pseudo,score_joueur)
    return data_base

def fermer_win():
    '''
    Permet de fermer la fenêtre où on entre son pseudo

    '''      
    while True:
        event, values = window.read()
        if event == 'Fermer' or event in (sg.WIN_CLOSED, 'Exit'):
            break

#----Affichage perdu ou gagné----
resume=False

if score_bot != 'stop' and score_joueur != 'stop':   
    if score_bot < score_joueur:
        pygame.mixer.Sound("victoir.mp3").play()      
        score_tot = 'Avec un score de : '+str(score_joueur)
        layout_fin = [[sg.Txt('Vous avez gagné 👏 !!'),sg.Txt(score_tot)]]
        layout_fin += [[sg.Txt('Entrez votre pseudo : '), 
                        sg.In(size=(12,1), key='pseudo_entrer')]]
        layout_fin += [[sg.Ok("Entrer"), sg.Txt('', key=('res'), size=(30,2))]]
        layout_fin += [[sg.Button('Fermer')]]
    if score_bot > score_joueur:
        pygame.mixer.Sound("perdu.mp3").play()
        layout_fin = [[sg.Txt("Vous avez perdu 😭",size=(22,1))]]
   
    window = sg.Window('Résultat', layout=layout_fin)
    
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'Entrer':
            pseudo = values['pseudo_entrer']
            data_base = resultat(pseudo,score_joueur)
            fermer_win()
            resume = True  
            break          
    window.close()

#----Affichage Base de données----

if resume==True:
    longeur_data = 20
    if len(data_base)<20:
        longeur_data = len(data_base)
    layout_data = [[sg.T('Base de données (affiche les 20 premiers max):')]]
    layout_data += [[sg.T(data_base[i].lower(), size=(30, 1))] for i in range(longeur_data)]
    window = sg.Window('Base de données', layout=layout_data)
    
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

window.close()