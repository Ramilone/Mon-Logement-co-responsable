-----------------------------------------------------------------------------
-- ORDRES PERMETTANT DE DÉTRUIRE TOUTES LES TABLES EXISTANTES DANS LA BASE --
-----------------------------------------------------------------------------

-- Entités -- 
DROP TABLE IF EXISTS Facture; 
DROP TABLE IF EXISTS Mesure; 
DROP TABLE IF EXISTS Type_t; 
DROP TABLE IF EXISTS Capteur; 
DROP TABLE IF EXISTS Piece; 
DROP TABLE IF EXISTS Logement; 



-----------------------------------------------------------------
-- ORDRES PERMETTANT DE CRÉER LES TABLES DU MODÈLE RELATIONNEL -- 
-----------------------------------------------------------------

-- pense à ajouter des commentaires expliquant les ajouts dans le code pour les questions 4 à 8 de la partie 1 

-- Création des Entités -- 
CREATE TABLE Logement (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        ip TEXT NOT NULL, 
                        adresse TEXT NOT NULL, 
                        date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        numero_telephone TEXT NOT NULL);  

CREATE TABLE Facture (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nature TEXT NOT NULL, 
                        date_facture TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                        montant FLOAT,
                        valeur_consommee FLOAT,
                        id_logement INTEGER, 
                        FOREIGN KEY (id_logement) REFERENCES Logement(id));   

CREATE TABLE Piece (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    nom TEXT NOT NULL,
                    coordonnees TEXT NOT NULL,
                    id_logement INTEGER, 
                    FOREIGN KEY (id_logement) REFERENCES Logement(id));   

CREATE TABLE Capteur (ref_commercial TEXT PRIMARY KEY, 
                        ref_coordonnee TEXT NOT NULL, 
                        date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                        unite_mesure TEXT NOT NULL, 
                        id_piece INTEGER,
                        FOREIGN KEY (unite_mesure) REFERENCES Type_t(unite),
                        FOREIGN KEY (id_piece) REFERENCES Piece(id));  

CREATE TABLE Type_t (unite TEXT PRIMARY KEY, 
                    precision_t TEXT); 

CREATE TABLE Mesure (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    valeur FLOAT,
                    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                    sn_capteur TEXT NOT NULL, 
                    FOREIGN KEY (sn_capteur) REFERENCES Capteur(ref_commercial));   
  

------------------------------------------------------------
------- REMPLISSAGE DE LA BASE DE DONNÉES POUR TESTS ------- 
------------------------------------------------------------

-- Pour la partie Test, 3 logements et leurs factures d'eau, de gaz et d'électricité par mois pendant 1 an

-- 3 logements
INSERT INTO Logement (ip, adresse, numero_telephone) VALUES 
    ('192.168.15.101', '4 Place Jussieu, Paris 75005', '06 12 34 56 78'),     -- premier logement
    ('10.0.5.78', '38 boulevard Soult, Paris 75012', '07 98 76 54 32'),       -- deuxième logement
    ('172.16.254.3', '47 rue des Cités, Chelles 77500', '01 23 45 67 89');    -- troisième logement


-- Factures d'électricité sur une année pour le premier logement 
INSERT INTO Facture (nature, date_facture, montant, valeur_consommee, id_logement) VALUES
    ('Électricité', '2024-01-31', 559.31, 2223, 1),
    ('Électricité', '2024-02-28', 489.20, 1948, 1),
    ('Électricité', '2024-03-31', 512.45, 2021, 1),
    ('Électricité', '2024-04-30', 473.75, 1875, 1), 
    ('Électricité', '2024-05-31', 502.10, 1992, 1),
    ('Électricité', '2024-06-30', 530.30, 2100, 1),
    ('Électricité', '2024-07-31', 601.50, 2406, 1),
    ('Électricité', '2024-08-31', 587.75, 2351, 1),
    ('Électricité', '2024-09-30', 543.60, 2174, 1),
    ('Électricité', '2024-10-31', 509.40, 2037, 1),
    ('Électricité', '2024-11-30', 479.85, 1919, 1),
    ('Électricité', '2024-12-31', 526.95, 2108, 1);

-- Factures d'eau sur une année pour le premier logement 
INSERT INTO Facture (nature, date_facture, montant, valeur_consommee, id_logement) VALUES
    ('Eau', '2024-01-31', 234.36, 54, 1), 
    ('Eau', '2024-02-28', 210.45, 49, 1),
    ('Eau', '2024-03-31', 225.78, 52, 1),
    ('Eau', '2024-04-31', 198.12, 46, 1),
    ('Eau', '2024-05-31', 240.65, 56, 1),
    ('Eau', '2024-06-31', 253.89, 59, 1),
    ('Eau', '2024-07-31', 271.34, 63, 1),
    ('Eau', '2024-08-31', 265.22, 62, 1), 
    ('Eau', '2024-09-31', 249.87, 58, 1),
    ('Eau', '2024-10-31', 233.19, 54, 1),
    ('Eau', '2024-11-31', 220.45, 51, 1),
    ('Eau', '2024-12-31', 245.60, 57, 1);

-- Factures de gaz sur une année pour le premier logement 
INSERT INTO Facture (nature, date_facture, montant, valeur_consommee, id_logement) VALUES 
    ('Gaz', '2024-01-31', 363.20, 3323, 1), 
    ('Gaz', '2024-02-28', 335.40, 3105, 1), 
    ('Gaz', '2024-03-31', 345.75, 3200, 1),
    ('Gaz', '2024-04-30', 312.60, 2890, 1),
    ('Gaz', '2024-05-31', 298.45, 2750, 1),
    ('Gaz', '2024-06-30', 278.90, 2600, 1),
    ('Gaz', '2024-07-31', 255.60, 2395, 1),
    ('Gaz', '2024-08-31', 249.85, 2340, 1),
    ('Gaz', '2024-09-30', 265.30, 2455, 1),
    ('Gaz', '2024-10-31', 300.75, 2775, 1),
    ('Gaz', '2024-11-30', 322.90, 2990, 1),
    ('Gaz', '2024-12-31', 348.25, 3220, 1);


-- Une pièce dans le premier logement
INSERT INTO Piece (nom, coordonnees, id_logement) VALUES
    ('Salon', '(x,y,z)', 1); 
