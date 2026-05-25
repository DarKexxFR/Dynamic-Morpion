import tkinter as tk
import random

plateau = [' ' for _ in range(9)]
joueur = 'X'
positions_X = []
positions_O = []
couleurs = {
    'X': "#FF5733",
    'O': "#33C3FF"
}
mode_jeu = 'local'
niveau_bot = None

# Fonction pour lancer le jeu local
def lancer_jeu_local():
    global mode_jeu
    mode_jeu = 'local'
    initialiser_jeu()
    fenetre_selection.withdraw()

# Fonction pour lancer le jeu contre le bot
def lancer_jeu_bot(niveau):
    global mode_jeu, niveau_bot
    mode_jeu = 'bot'
    niveau_bot = niveau
    initialiser_jeu()
    fenetre_selection.withdraw()

# Fonction pour initialiser le jeu
def initialiser_jeu():
    global root, label_joueur, label_message, boutons, bouton_recommencer
    root = tk.Tk()
    root.title("Jeu du Morpion")

    global plateau, joueur, positions_X, positions_O
    plateau = [' ' for _ in range(9)]
    joueur = 'X'
    positions_X = []
    positions_O = []

    label_joueur = tk.Label(root, text="Tour du joueur X", font=("Helvetica", 14), pady=10)
    label_joueur.grid(row=0, column=0, columnspan=3)

    label_message = tk.Label(root, text="", font=("Helvetica", 12), fg="green", pady=10)
    label_message.grid(row=4, column=0, columnspan=3)

    global boutons
    boutons = []
    for i in range(9):
        bouton = tk.Button(
            root, text=' ', width=10, height=3,
            font=("Helvetica", 20),
            bg="#ECECEC",
            activebackground="#D0D0D0",
            command=lambda i=i: clic_bouton(i, boutons[i])
        )
        bouton.grid(row=(i // 3) + 1, column=i % 3, padx=5, pady=5)
        boutons.append(bouton)

    bouton_recommencer = tk.Button(root, text="Recommencer", font=("Helvetica", 14), command=menu_recommencer)
    bouton_recommencer.grid(row=5, column=0, columnspan=3, pady=10)
    bouton_recommencer.grid_remove()

    root.mainloop()

# Fonction pour gérer les clics sur les boutons
def finish_game(winner):
    label_message.config(text=f"Le joueur {winner} a gagné !")
    desactiver_boutons()
    bouton_recommencer.grid()


def clic_bouton(index, bouton):
    global joueur

    if plateau[index] == ' ':
        plateau[index] = joueur
        bouton.config(text=joueur, fg=couleurs[joueur])

        if joueur == 'X':
            positions_X.append(index)
            if len(positions_X) > 3:
                retirer_premier_symbole(positions_X, 'X')
            if verifier_victoire():
                finish_game(joueur)
                return
            joueur = 'O'
            label_joueur.config(text=f"Tour du joueur {joueur}")
            if mode_jeu == 'bot':
                jouer_bot()

        else:
            positions_O.append(index)
            if len(positions_O) > 3:
                retirer_premier_symbole(positions_O, 'O')
            if verifier_victoire():
                finish_game(joueur)
                return
            joueur = 'X'
            label_joueur.config(text=f"Tour du joueur {joueur}")

# Fonction pour jouer le bot
def jouer_bot():
    global joueur
    if joueur != 'O':
        return

    empty_cells = [i for i in range(9) if plateau[i] == ' ']
    if not empty_cells:
        return

    if niveau_bot == 1:
        index = random.choice(empty_cells)
    elif niveau_bot == 2:
        index = bloquer_joueur()
    else:
        index = random.choice(empty_cells)

    if index is None:
        return

    plateau[index] = joueur
    boutons[index].config(text=joueur, fg=couleurs[joueur])

    positions_O.append(index)
    if len(positions_O) > 3:
        retirer_premier_symbole(positions_O, 'O')
    if verifier_victoire():
        finish_game(joueur)
        return
    joueur = 'X'
    label_joueur.config(text=f"Tour du joueur {joueur}")

# Fonction pour bloquer le joueur
def bloquer_joueur():
    for combinaison in [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                        [0, 3, 6], [1, 4, 7], [2, 5, 8],
                        [0, 4, 8], [2, 4, 6]]:
        if plateau[combinaison[0]] == plateau[combinaison[1]] == 'X' and plateau[combinaison[2]] == ' ':
            return combinaison[2]
        if plateau[combinaison[1]] == plateau[combinaison[2]] == 'X' and plateau[combinaison[0]] == ' ':
            return combinaison[0]
        if plateau[combinaison[0]] == plateau[combinaison[2]] == 'X' and plateau[combinaison[1]] == ' ':
            return combinaison[1]
    empty = [i for i in range(9) if plateau[i] == ' ']
    return random.choice(empty) if empty else None

# Fonction pour retirer le premier symbole
def retirer_premier_symbole(positions, symbole):
    if positions:
        premier_index = positions.pop(0)
        plateau[premier_index] = ' '
        boutons[premier_index].config(text=' ')

# Fonction pour désactiver tous les boutons après la fin du jeu
def desactiver_boutons():
    for bouton in boutons:
        bouton.config(state=tk.DISABLED)

# Fonction pour afficher le menu de recommencement
def menu_recommencer():
    global bouton_local, bouton_niveau1, bouton_niveau2
    for bouton in boutons:
        bouton.config(state=tk.NORMAL)
    label_message.config(text="")

    fenetre_recommencer = tk.Toplevel(root)
    fenetre_recommencer.title("Sélection du mode de jeu")

    bouton_local = tk.Button(fenetre_recommencer, text="Jouer en local", command=lancer_jeu_local, font=("Helvetica", 14))
    bouton_local.pack(pady=10)

    label_niveau = tk.Label(fenetre_recommencer, text="Choisir le niveau du bot :", font=("Helvetica", 14))
    label_niveau.pack(pady=10)

    bouton_niveau1 = tk.Button(fenetre_recommencer, text="Niveau 1 (Aléatoire)", command=lambda: lancer_jeu_bot(1), font=("Helvetica", 14))
    bouton_niveau1.pack(pady=5)

    bouton_niveau2 = tk.Button(fenetre_recommencer, text="Niveau 2 (Bloque le joueur)", command=lambda: lancer_jeu_bot(2), font=("Helvetica", 14))
    bouton_niveau2.pack(pady=5)

# Fonction pour vérifier s'il y a un gagnant
def verifier_victoire():
    combinaisons_victoire = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combinaison in combinaisons_victoire:
        if plateau[combinaison[0]] == plateau[combinaison[1]] == plateau[combinaison[2]] != ' ':
            return True
    return False

# Création de la fenêtre de sélection
fenetre_selection = tk.Tk()
fenetre_selection.title("Sélection du mode de jeu")

bouton_local = tk.Button(fenetre_selection, text="Jouer en local", command=lancer_jeu_local, font=("Helvetica", 14))
bouton_local.pack(pady=10)

label_niveau = tk.Label(fenetre_selection, text="Choisir le niveau du bot :", font=("Helvetica", 14))
label_niveau.pack(pady=10)

bouton_niveau1 = tk.Button(fenetre_selection, text="Niveau 1 (Aléatoire)", command=lambda: lancer_jeu_bot(1), font=("Helvetica", 14))
bouton_niveau1.pack(pady=5)

bouton_niveau2 = tk.Button(fenetre_selection, text="Niveau 2 (Bloque le joueur)", command=lambda: lancer_jeu_bot(2), font=("Helvetica", 14))
bouton_niveau2.pack(pady=5)

fenetre_selection.mainloop()
