import sqlite3
import random
from flask import Flask, request, jsonify


# ouverture/initialisation de la base de donnee 
conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Nombre de factures/mesures que l'on souhaite générer
n = 10

#########################################################
######################## PARTIE 1 ####################### 
#########################################################

# Insertion d'un nouveau logement dans la table Logement
c.execute("INSERT INTO Logement VALUES (1, '127.0.0.1', '9 rue Gay Lussac', '2024-11-15', '0754820335', 1, 1)") 

# Insertion d'une pièce dans la table Piece qui appartienne au logement créé précédemment
c.execute("INSERT INTO Piece VALUES (1, 'piece_test', '(0,0,0)', 1, 1)") 

# Insertion d'un type dans la table Type_t 
c.execute("INSERT INTO Type_t VALUES ('degre', '0.5')")

# Insertion d'un capteur dans la table Capteur qui appartienne à la pièce créée précédemment
c.execute("INSERT INTO Capteur VALUES('azerty12345', 'capteur_test', '2024-11-15', 'degre')")


# Insertion de plusieurs factures dans la table Facture du logement créé précédemment
factures = []
for i in range(n): 
    f = random.randint(1, 1000)
    factures.append((i, '2024-11-15', f, f*3)) 
    f = 0 
c.executemany("INSERT INTO Facture VALUES(?, ?, ?, ?)", factures) 

# Insertion de plusieurs mesures dans la table Mesure du capteur créé précédemment
mesures = []
for i in range(n): 
    m = random.uniform(-10, 50)
    mesures.append((i, m))
    m = 0
c.executemany("INSERT INTO Mesure VALUES(?, ?, '2024-11-15', 'azerty12345')", mesures) 


# Lecture dans la base avec un select
c.execute('SELECT * FROM Logement')
print(c.fetchall()) 



#########################################################
######################## PARTIE 2 ####################### 
#########################################################


# class Logement(BaseModel):
#     id: int
#     ip: str
#     adresse: str
#     date_insertion: str
#     tel: str
    

# class Facture(BaseModel):
#     id: int
#     date_facture: str
#     montant: float
#     valeur_consommee: float
#     id_logement: int


# class Piece(BaseModel):
#     id: int
#     nom: str
#     coordonnes: str
#     id_logement: str


# class Capteur(BaseModel):
#     ref_commercial: str
#     ref_coordonnee: str
#     date_insertion: str
#     unite_mesure: str
#     id_piece: int 


# class Type_t(BaseModel):
#     unite: str
#     precision_t: str


# class Mesure(BaseModel):
#     id: int
#     valeur: float
#     date_insertion: str
#     id_capteur: str 



# # Requête POST: ajouter un logement
# @app.route("/Logement", methods=["POST"])
# async def create_logement(logement: Logement):
#     return logement 

# # Requête POST: ajouter une facture
# @app.route("/Facture", methods=["POST"])
# async def create_facture(facture: Facture):
#     return facture 

# # Requête POST: ajouter une pièce
# @app.route("/Piece", methods=["POST"])
# async def create_piece(piece: Piece):
#     return piece 

# # Requête POST: ajouter un capteur
# @app.route("/Capteur", methods=["POST"])
# async def create_capteur(capteur: Capteur):
#     return capteur

# # Requête POST: ajouter un type
# @app.route("/Type_t", methods=["POST"])
# async def create_type(type: Type_t):
#     return type

# # Requête POST: ajouter une mesure
# @app.route("/Mesure", methods=["POST"])
# async def create_mesure(mesure: Mesure):
#     return mesure



# fermeture
conn.commit()
conn.close()
