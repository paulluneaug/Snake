import tkinter as tk
from random import choice

def play_snake():
    """
    Lance une partie de Snake

    Controles :

        -Flèches directionelles pour orienter le serpent
        -m
    """
    global c,x_can,y_can,speed,fen,can,fruit,snake,dir_changeable,pts,lab_pts

    x_can,y_can=25,25 #Nombre de case en largeur et en hauteur de la grille sur
                      #laquelle le serpent se déplace

    c=600//max(x_can,y_can) #Taille en pixels de chaque case
    speed=100 #Temps en ms entre chaque mise à jour de la grille
    dir_changeable=True #Indique que le serpent peut changer de direction


    fen=tk.Tk()
    fen.title('Snake')


    lab_pts=tk.Label(fen,text=f'Score : {pts}',font='candara 12',fg='black')
    lab_pts.grid(column=0,row=0)

    can=tk.Canvas(width=x_can*c,height=y_can*c,bg='black')
    can.grid(column=0,row=1)

    snake=[[(0,0),(1,0),(2,0),(3,0)],(1,0)] #Liste indiquant l'état du serpent
                          #Elle est composée d'une liste des tuples pour chaque
                          #case de la grille sur laquelle on trouve un morceau
                          #de serpent
                          #et d'un tuple de 2 valeurs représentant la direction
                          #dans laquelle part le serpent
    pts=0

    fen.bind('<Left>',lambda x: change_dir((-1,0)))
    fen.bind('<Right>',lambda x: change_dir((1,0)))
    fen.bind('<Up>',lambda x: change_dir((0,-1)))
    fen.bind('<Down>',lambda x: change_dir((0,1)))
    fen.bind('<m>',restart)

    replace_fruit()
    can_update(update_fruit=True)

    play()

    fen.mainloop()

def change_dir(tup):
    """
    Change le tuple qui indique la direction du serpent
    """
    global dir_changeable
    if dir_changeable: #On vérifie que le serpent n'a pas déjà changé de sens
        if snake[1][0]!=-tup[0] and snake[1][1]!=-tup[1]: #Et qu'il ne veut pas
                                                          #se retourner de 180°
            snake[1]=tup
            dir_changeable=False

def can_update(update_fruit=False):
    """
    Met à joue le canvas pour afficher la nouvelle position du serpent
    """
    can.delete('snake')
    len_snake=len(snake[0])
    for p in range(len_snake):
        pix=snake[0][p]
        can.create_rectangle(pix[0]*c,pix[1]*c,pix[0]*c+c,pix[1]*c+c,fill='lime',outline='lime',tag='snake')
##    for p in range (len_snake):
##        pix=snake[0][p]
##        pad=0.07+((len_snake-p-1)/len_snake)*0.2 #Diminue la taille de chaque
##        #case du serpent selon sa position dans la liste, donc selon son
##        #éloignement à la tête
##        can.create_rectangle((pix[0]+pad)*c,(pix[1]+pad)*c,(pix[0]+1-pad)*c,
##                             (pix[1]+1-pad)*c,fill='lime',tag='snake')

    #Place 2 yeux sur la tête du serpent pour indiquer rapidement dans quelle
    #direction va le serpent

    head=snake[0][-1] #Identifie la tête du serpent

    eye_size=c/7 #Indique la taille des yeux
    frac=1/4

    dict_eye={(-1,0):[(frac,frac),(frac,1-frac)],   #Dictionnaire liant chaque
              (1,0):[(1-frac,frac),(1-frac,1-frac)],#direction à la position des
              (0,1):[(frac,1-frac),(1-frac,1-frac)],#2 yeux sur la tête du
              (0,-1):[(frac,frac),(1-frac,frac)]}   #serpent

    eye_pos=dict_eye[snake[1]]

    for eye in range(2): #Place les 2 yeux
        can.create_oval((head[0]+eye_pos[eye][0])*c-eye_size,
                        (head[1]+eye_pos[eye][1])*c-eye_size,
                        (head[0]+eye_pos[eye][0])*c+eye_size,
                        (head[1]+eye_pos[eye][1])*c+eye_size,
                        fill='red',tag='snake')

    if update_fruit: #Change la position du fruit si besoin
        can.delete('fruit')
        can.create_oval((fruit[0]+0.1)*c,(fruit[1]+0.1)*c,(fruit[0]+0.9)*c,
                        (fruit[1]+0.9)*c,fill='red',tag='fruit')


def play():
    """
    Boucle principale du jeu
    """
    global dir_changeable
    #Calcule la prochaine position de la tête du serpent
    next_pix=(snake[0][-1][0]+snake[1][0],snake[0][-1][1]+snake[1][1])
    print(snake)

    #Vérifie que la tête ne touche pas un bord ou la queue du serpent
    if next_pix in [(a,b) for a in range(x_can) for b in range(y_can)] and not next_pix in snake[0]:
        if next_pix!=fruit:
            snake[0].pop(0)
        else:               #Si la tête touche un fruit, re-place le fruit
            replace_fruit() #et agrandit le serpent
        snake[0].append(next_pix)
        can_update(update_fruit=True)
        dir_changeable=True
        fen.after(speed,play)
    else:
        lose()



def replace_fruit():
    """
    Place un nouveau fruit sur la grille
    """
    global fruit,pts
    #Dresse la liste des cases vides et place la fruit aléatoirement parmi cette
    #liste
    list_empty=[pix for pix in [(a,b) for a in range(x_can) for b in range(y_can)] if pix not in snake[0]]
    fruit=choice(list_empty)
    pts+=1
    lab_pts.configure(text=f'Score : {pts}')

def lose():
    """
    Indique au joueu.r.se qu'il.elle a perdu
    """
    can_update()
    can.create_text(x_can*c/2,y_can*c/2-20,text='Perdu',font='Verdana 20',
                    fill='white')
    can.create_text(x_can*c/2,y_can*c/2+20,font='Verdana 15',fill='white',
                    text='Appuyez sur M pour recommencer')

def restart(event):
    """
    Recommence une partie
    """
    fen.destroy()
    play_snake()

play_snake()