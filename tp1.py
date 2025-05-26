

import mysql.connector
import tkinter as tk
import os
from tkinter import messagebox, ttk

# Connexion à la base MySQL
def get_conn():
 return mysql.connector.connect(
host="localhost",
user="root", 
password= environ.get("MYSQL_PASSWORD"),
database="helpdesk"
)

def ajouter_utilisateur():
 nom = entry_nom.get()
 email = entry_email.get()

 conn = get_conn()
 cursor = conn.cursor()
 cursor.execute("INSERT INTO utilisateur (nom, email) VALUES (%s, %s)", (nom, email))
 conn.commit()
 conn.close()
 messagebox.showinfo("Succès", "Utilisateur ajouté.")

def creer_ticket():
    titre = entry_titre.get()
    description = entry_description.get("1.0", tk.END).strip()
    id_user = entry_id_user.get()

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ticket (titre, description, id_utilisateur) VALUES (%s, %s, %s)",
        (titre, description, id_user))
    conn.commit()
    conn.close()
    messagebox.showinfo("Succès", "Ticket créé.")




def lister_tickets():
    for item in tree.get_children():
        tree.delete(item)

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.id, t.titre, t.statut, u.nom, t.date_creation
        FROM ticket t JOIN utilisateur u ON t.id_utilisateur = u.id
        ORDER BY t.date_creation DESC
    ''')

    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

    conn.close()


root = tk.Tk()
root.title("Application Helpdesk")

tk.Label(root, text="Nom").grid(row=0, column=0)
entry_nom = tk.Entry(root)
entry_nom.grid(row=0, column=1)

tk.Label(root, text="Email").grid(row=1, column=0)
entry_email = tk.Entry(root)
entry_email.grid(row=1, column=1)

tk.Button(root, text="Ajouter utilisateur", command=ajouter_utilisateur).grid(row=2, column=0, columnspan=2, pady=5)


tk.Label(root, text="Titre").grid(row=3, column=0)
entry_titre = tk.Entry(root)
entry_titre.grid(row=3, column=1)

tk.Label(root, text="Description").grid(row=4, column=0)
entry_description = tk.Text(root, height=4, width=30)
entry_description.grid(row=4, column=1)

tk.Label(root, text="ID Utilisateur").grid(row=5, column=0)
entry_id_user = tk.Entry(root)
entry_id_user.grid(row=5, column=1)

tk.Button(root, text="Créer ticket", command=creer_ticket).grid(row=6, column=0, columnspan=2, pady=5)


tk.Label(root, text="Tickets").grid(row=7, column=0, columnspan=2)
tree = ttk.Treeview(root, columns=("ID", "Titre", "Statut", "Utilisateur", "Date"), show="headings")
tree.grid(row=8, column=0, columnspan=2)

for col in ("ID", "Titre", "Statut", "Utilisateur", "Date"):
 tree.heading(col, text=col)

tk.Button(root, text="Rafraîchir la liste", command=lister_tickets).grid(row=9, column=0, columnspan=2, pady=5)

root.mainloop()