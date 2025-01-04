###########################
## PAGE DE GARDE DU SITE ##
###########################

from flask import Flask, request, redirect, jsonify, render_template_string
import sqlite3
from datetime import datetime
import requests
import json

app = Flask(__name__) 
def connect_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row          
    return conn


# Route GET gérant la page de connexion du site
@app.route('/site/login', methods=['GET'])
def login_page():
    template = """

    <!DOCTYPE html>
    <html>
    <head>
        <title>Connexion</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
        <style>
            body{
                background-color: #f8f9fa;
            }
            h1{
                color: #343a40;
                text-align: center;
            }
            p{
                text-align: center;
            }
            .form-container {
                max-width: 400px;
                margin: 50px auto;
                padding: 20px;
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
        </style>
    </head>
    <body>
        <h1>Page de Connexion</h1>
        <p>Bienvenue sur la page de connexion. Veuillez entrer vos identifiants.</p>

        <div class="form-container">
        <form method="POST" action="/verifier_identifiant">
            <div class="form-group">
                <label for="identifiant">Identifiant :</label>
                <input type="number" class="form-control" id="identifiant" name="identifiant" placeholder="Entrez votre identifiant" required>
            </div>
            <button type="submit" class="btn btn-success btn-block">Se connecter</button>
        </form>
    </div>
    </body>
    </html>

    """
    return template

# Route POST vérifiant la validité de l'identifant et redirigeant vers l'espace client du logement concerné
@app.route('/verifier_identifiant', methods=['POST'])
def verifier_identifiant():
    # Récupérer l'identifiant du formulaire
    identifiant = request.form.get('identifiant')
    if not identifiant:
        return "Identifiant non fourni", 400  # Erreur de requête (Bad Request)
    try:
        # Convertir l'identifiant en entier
        identifiant = int(identifiant)
    except ValueError:
        return "Identifiant invalide, veuillez entrer un entier.", 400
    
    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    try:    
        # Vérifier si l'identifiant existe dans la table Facture
        c.execute("SELECT * FROM Logement WHERE id = ?", (identifiant,))
        result = c.fetchall()  # Utilisez fetchall() pour récupérer tous les enregistrements associés

        if result:  # Si la liste result n'est pas vide
            # Si l'identifiant existe, rediriger vers la page correspondante
            return redirect(f"/site/mon_espace_client/{identifiant}")
        else:
            # Identifiant non trouvé
            return "Identifiant non reconnu", 404
    finally:
        # Fermer la connexion à la base de données
        conn.close()


# Route GET gérant la page principale de l'espace client, donnant accès aux autres fonctionnalités via des boutons
@app.route('/site/mon_espace_client/<int:id>', methods=['GET'])
def lobby(id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT adresse, ip, numero_telephone FROM Logement WHERE id = ?", (id,))

    logement = c.fetchone()
    conn.close()
    ip = logement['ip']
    adresse = logement['adresse']
    numero_telephone = logement['numero_telephone']

    template = """

    <!DOCTYPE html>
    <html>
    <head>
        <title> Mon Logement Éco-responsable </title>   
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>    
        <style>
            body {
                font-family: Arial, Helvetica, sans-serif;
            }
            header{
                background-color: #95f573;
                color: white; 
                text-align: center; 
                padding: 30px; 
            }
            nav{
                text-align: center; 
                float: left;
                width: 30%; 
                heigth: 50px;
                background: #d1d1d1; 
                padding: 20px; 
                box-sizing: border-box; 
            }
            nav ul {
                list-style-type: none;
                padding: 0;
            }
            nav ul li {
                margin-top: 20px; 
            }
            nav ul li a {
                text-decoration: none;
                font-size: 18px; 
                color: #000; 
            }
            nav ul li a:hover {
                font-size: 20px; 
                color: #0066cc; 
            }
            article {
                float: left;
                width: 70%;
                heigth: 3000px;
                background: white; 
                font-size: 18px;
                padding: 20px; 
                box-sizing: border-box; 
            }
            @media (max-width: 600px) {
                nav, article {
                    width: 100%;
                    height: auto;
                }
            }
        </style>
    </head>
    <body>
        <header>
        <h1> Mon Logement Éco-Responsable </h1>
        </header>
        <section>
            <nav>
                <ul>
                <li><a href="/site/mon_espace_client/{{ id }}/ma_consommation"> Ma Consommation </a></li>
                <li><a href="/site/mon_espace_client/{{ id }}/etat_devices"> Mes Capteurs/Actionneurs </a></li>
                <li><a href="/site/mon_espace_client/{{ id }}/mes_economies"> Mes Économies </a></li>
                <li><a href="/site/mon_espace_client/{{ id }}/configuration"> Configuration </a></li>
                </ul>
            </nav>
        </section>
        <article>
            <p>
                <h2>Mon Logement Éco-Responsable</h2> est la solution pour contrôler sa consommation grâce à l'Internet of Things. 
            </p>
            <p>
                <h2> Les informations de mon logement: </h2>
            </p>
            <p>
                    <li> <strong>Adresse:</strong> {{ adresse }} </li>
                    <li> <strong>Adresse IP:</strong> {{ ip }}  </li>
                    <li> <strong>Numéro de Téléphone:</strong> {{ numero_telephone }}  </li>
            </p>
        </article>
    </body>
    </html>

    """
    return render_template_string(template, id=id, adresse=adresse, ip=ip, numero_telephone=numero_telephone)



# Route GET gérant la page web contenant le graphique de la consommation d'un logement en fonction de la durée de temps sélectionnée
@app.route('/site/mon_espace_client/<int:id_logement>/ma_consommation', methods=['GET'])
def ma_consommation(id_logement):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT strftime('%Y-%m', date_facture) AS mois, nature, valeur_consommee FROM Facture WHERE id_logement = ? ORDER BY mois ASC, nature", (id_logement,))
    title = f"Votre consommation d'Électricité, d'Eau et de Gaz ces derniers mois"

    Conso = c.fetchall()
    conn.close()

    # Organiser les données par mois
    mois_data = {}
    for facture in Conso:
        mois = facture['mois']
        nature = facture['nature']
        valeur = facture['valeur_consommee']
        
        if mois not in mois_data:
            mois_data[mois] = {'Électricité': None, 'Eau': None, 'Gaz': None}
        
        mois_data[mois][nature] = valeur
    
    # Préparer les données pour le graphique
    conso_graph_elec = [["Mois", "Électricité", "Eau", "Gaz"]]
    for mois, consos in mois_data.items():
        conso_graph_elec.append([mois, consos['Électricité'] or 0, consos['Eau'] or 0, consos['Gaz'] or 0])

    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
        google.charts.load('current', {'packages':['corechart']});
        google.charts.setOnLoadCallback(drawChart);

        function drawChart() {
            var data = google.visualization.arrayToDataTable({{ data|safe }});
            var options = {
                title: '{{ title }}',
                legend: { position: 'bottom' },
                curveType: 'function',
                vAxis: { title: 'Consommation' },
                hAxis: { title: 'Mois' }
            };
            var chart = new google.visualization.LineChart(document.getElementById('curve_chart')); 
            chart.draw(data, options);
        }
        </script>
    </head>
    <body>
        <h2>{{ title }}</h2>
        <div id="curve_chart" style="width: 900px; height: 500px"></div>
    </body>
    </html>
    """

    return render_template_string(template, data=conso_graph_elec, title=title)


# Route GET gérant la page web contenant les informations sur les différents capteurs déployés dans l'appartement concerné
# Route GET gérant la page web contenant les graphique des économies réalisées sous forme de comparatifs 



# Route GET gérant la page web des paramètres 
@app.route('/site/mon_espace_client/<int:id_logement>/configuration', methods=['GET'])
def param(id_logement):
    
    template = """"
    
    <!DOCTYPE html>
    <html>
    <head>
        <title> Paramètre </title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
    <style>
        body{
            background-color: #f8f9fa;
        }
        h1{
            color: #343a40;
            text-align: center; 
        }
        p{
            text-align: center;
        }
    </style>
    </head>
    <body>
        <h1> Paramètres </h1>
        <li><a href="/site/mon_espace_client/{{ id_logement }}/configuration/ajouter_capteur"> Ajouter Capteur </a></li>
    </body>
    </html>

    """
    return render_template_string(template, id_logement=id_logement)

# Route POST permettant d'ajouter un nouveau capteur/actionneur dans la page des paramètres
@app.route('/site/mon_espace_client/<int:id_logement>/configuration/ajouter_capteur', methods=['GET', 'POST'])
def ajout(id_logement):
    if request.method == 'POST':
        # Récupération des données envoyées dans le formulaire
        ref_commercial = request.form.get('ref_commercial')
        ref_coordonnee = request.form.get('ref_coordonnee')
        unite_mesure = request.form.get('unite_mesure')
        id_piece = request.form.get('id_piece')

        # Vérification des données
        if not all([ref_commercial, ref_coordonnee, unite_mesure, id_piece]):
            return jsonify({"error": "Tous les champs (ref_commercial, ref_coordonnee, unite_mesure, id_piece) sont requis."}), 400

        try:
            # Connexion à la base de données
            conn = sqlite3.connect('database.db')
            c = conn.cursor()

            # Insertion dans la table Capteur
            c.execute("INSERT INTO Capteur (ref_commercial, ref_coordonnee, unite_mesure, id_piece) VALUES (?, ?, ?, ?)", 
                      (ref_commercial, ref_coordonnee, unite_mesure, id_piece))

            conn.commit()
            conn.close()

            return jsonify({"message": "Capteur ajouté avec succès."}), 201

        except sqlite3.IntegrityError as e:
            return jsonify({"error": f"Erreur d'intégrité : {e}"}), 400

        except Exception as e:
            return jsonify({"error": f"Une erreur s'est produite : {e}"}), 500

    # Affichage du formulaire pour la méthode GET
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ajouter un Capteur</title>
    </head>
    <body>
        <h1>Ajouter un Capteur</h1>
        <form action="/site/mon_espace_client/{{ id_logement }}/configuration/ajouter_capteur" method="POST">
            <label for="ref_commercial">Référence Commerciale :</label>
            <input type="text" name="ref_commercial" id="ref_commercial" required><br>

            <label for="ref_coordonnee">Référence Coordonnée :</label>
            <input type="text" name="ref_coordonnee" id="ref_coordonnee" required><br>

            <label for="unite_mesure">Unité de Mesure :</label>
            <input type="text" name="unite_mesure" id="unite_mesure" required><br>

            <label for="id_piece">ID de la Pièce :</label>
            <input type="number" name="id_piece" id="id_piece" required><br>

            <button type="submit">Ajouter le Capteur</button>
        </form>
    </body>
    </html>
    """, id_logement=id_logement)



if __name__ == '__main__':
    app.run(debug=True)
