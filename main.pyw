from tkinter import *
import time

def mouse_button_down(event) :
    global grille
    if 0 < event.x < 500 and 0 < event.y < 500 :
        if int(bloc.get()) == 2 and grille.count(2) == 1 : grille[grille.index(2)] = 0
        elif int(bloc.get()) == 3 and grille.count(3) == 1 : grille[grille.index(3)] = 0
        grille[int((event.y//(500/taille))*taille+event.x//(500/taille))] = int(bloc.get())
    affich()

def key_down_return(event) :
    global taille
    try :
        taille = int(entree.get())
        crea_grille()
    except : a = 0

def recherche() :
    global texte
    try : texte.destroy()
    except : a = 0
    if grille.count(2)+grille.count(3) == 2 :
        r = [-1 for i in range (taille**2)]
        # -1 : case non visitées / 0 : départ / -2 : arrivée
        r[grille.index(2)],r[grille.index(3)],non,b = 0,-2,0,[]
        while non == 0 :
            non,m = 1,max(r)
            for i in range (len(r)) :
                if r[i] == m :
                    if i%taille != 0 and r[i-1] == -1 and grille[i-1] == 0 : r[i-1],non = m+1,0
                    if i >= taille and r[i-taille] == -1 and grille[i-taille] == 0 : r[i-taille],non = m+1,0
                    if i%taille != taille-1 and r[i+1] == -1 and grille[i+1] == 0 : r[i+1],non = m+1,0
                    if i < taille**2-taille and r[i+taille] == -1 and grille[i+taille] == 0 : r[i+taille],non = m+1,0
                    if i%taille != 0 and r[i-1] == -2 : b += [i-1]
                    elif i >= taille and r[i-taille] == -2 : b += [i-taille]
                    elif i%taille != taille-1 and r[i+1] == -2 : b += [i+1]
                    elif i < taille**2-taille and r[i+taille] == -2 : b += [i+taille]
                if len(b) == 1 :
                    non = 1
                    break
        if len(b) == 0 : texte = Label(cadre,text="Aucun chemin trouvé").pack(side=TOP,padx=5,pady=0)
        else :
            r[b[0]] = max(r)
            if b[0]%taille != 0 and r[b[0]-1] == r[b[0]] or b[0] >= taille and r[b[0]-taille] == r[b[0]] or b[0]%taille != taille-1 and r[b[0]+1] == r[b[0]] or b[0] < taille**2-taille and r[b[0]+taille] == r[b[0]] : r[b[0]] += 1
            while r[b[0]] != 0 :
                if b[0]%taille != 0 and r[b[0]-1] == r[b[0]]-1 : b = [b[0]-1]+b
                elif b[0] >= taille and r[b[0]-taille] == r[b[0]]-1 : b = [b[0]-taille]+b
                elif b[0]%taille != taille-1 and r[b[0]+1] == r[b[0]]-1 : b = [b[0]+1]+b
                elif b[0] < taille**2-taille and r[b[0]+taille] == r[b[0]]-1 : b = [b[0]+taille]+b
        b = b[1:-1]
        affich()
        affich2(b)

def crea_grille() :
    global grille
    grille = [0 for i in range (taille**2)]
    affich()

def affich() :
    canvas.delete("all")
    for i in range (taille+1) :
        canvas.create_line(i*(500/taille)+2,2,i*(500/taille)+2,502,width=1)
        canvas.create_line(2,i*(500/taille)+2,503,i*(500/taille)+2,width=1)
    [canvas.create_rectangle(j*(500/taille)+2,i*(500/taille)+2,(j+1)*(500/taille)+2,(i+1)*(500/taille)+2,fill="black",outline="black") if grille[i*taille+j] == 1 else canvas.create_rectangle(j*(500/taille)+2,i*(500/taille)+2,(j+1)*(500/taille)+2,(i+1)*(500/taille)+2,fill="blue",outline="blue") if grille[i*taille+j] == 2 else canvas.create_rectangle(j*(500/taille)+2,i*(500/taille)+2,(j+1)*(500/taille)+2,(i+1)*(500/taille)+2,fill="green",outline="green") if grille[i*taille+j] == 3 else "" for i in range (taille) for j in range (taille)]

def affich2(b) : [canvas.create_rectangle((i%taille)*(500/taille)+2,(i//taille)*(500/taille)+2,((i%taille)+1)*(500/taille)+2,(i//taille+1)*(500/taille)+2,fill="red",outline="red") for i in b]

fenetre = Tk()
fenetre.title("Pathfinding test")
fenetre.resizable(width=False,height=False)

canvas = Canvas(fenetre,width=501,height=501,bg="white")
canvas.pack(side=LEFT,padx=5,pady=5)
canvas.bind("<Button-1>",mouse_button_down)
canvas.bind("<B1-Motion>",mouse_button_down)

cadre = LabelFrame(fenetre,text="",padx=5,pady=5,borderwidth=0)
cadre.pack(side=LEFT,fill="both",expand="no")
taille = 10
entree = Entry(cadre,width=20)
entree.pack(side=TOP,anchor="w",padx=5,pady=5)
entree.bind("<Return>",key_down_return)
bloc = StringVar()
b_bloc0,b_bloc1,b_bloc2,b_bloc3 = Radiobutton(cadre,text="Gomme",variable=bloc,value=0,state=ACTIVE).pack(side=TOP,anchor="w",padx=5,pady=0),Radiobutton(cadre,text="Mur",variable=bloc,value=1,state=ACTIVE).pack(side=TOP,anchor="w",padx=5,pady=0),Radiobutton(cadre,text="Départ",variable=bloc,value=2,state=ACTIVE).pack(side=TOP,anchor="w",padx=5,pady=0),Radiobutton(cadre,text="Arrivée",variable=bloc,value=3,state=ACTIVE).pack(side=TOP,anchor="w",padx=5,pady=0)
bloc.set("0")
b_recherche = Button(cadre,text="Rechercher",command=recherche).pack(side=TOP,anchor="w",padx=5,pady=0)

crea_grille()

fenetre.mainloop()