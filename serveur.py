##################################
############ PARTIE 2 ############
##################################

# 2.1: l'objectif dans un premier temps est d'ajouter dans notre base de données quelques mesures et factures en utilisant des requêtes GET et POST
#       pour ajouter une nouvelle facture, il faut déjà avoir un logement
#       pour ajouter des mesures, il faut déjà un capteur, une pièce et un logement


from flask import Flask, request, jsonify, render_template_string
import sqlite3
from datetime import datetime
import requests  


app = Flask(__name__) 


# Connexion à la base de données 
def connect_db():
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row      # Permet d'accéder aux colonnes de notre base de données grâce à leur nom
    return conn 


# Route GET pour consulter l'ensemble des Logements
@app.route('/Logement', methods=['GET'])
def get_Logement():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM Logement")
    Logement = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in Logement])

# Route POST pour ajouter un nouveau Logement 
@app.route('/Logement', methods=['POST'])
def post_Logement():
    new_logement = request.json
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO Logement (id, ip, adresse, date_insertion, numero_telephone)
        VALUES (?, ?, ?, ?, ?)
    ''', (new_logement['id'], new_logement['ip'], new_logement['adresse'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), new_logement['numero_telephone']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Nouveau logement enregistrée"}), 201 



# Route GET pour consulter l'ensemble des pièces
@app.route('/Piece', methods=['GET'])
def get_Piece():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM Piece")
    Piece = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in Piece])

# Route POST pour ajouter une nouvelle Piece
@app.route('/Piece', methods=['POST'])
def post_Piece():
    new_piece = request.json
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO Piece (id, nom, coordonnees, id_logement)
        VALUES (?, ?, ?, ?)
    ''', (new_piece['id'], new_piece['nom'], new_piece['coordonnees'], new_piece['id_logement']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Nouvelle Pièce enregistrée"}), 201



# Route GET pour consulter l'ensemble des capteurs
@app.route('/Capteur', methods=['GET'])
def get_capteur():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM Capteur")
    Capteur = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in Capteur])

# Route POST pour ajouter un nouveau capteur
@app.route('/Capteur', methods=['POST'])
def post_capteur():
    new_capteur = request.json
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO Capteur (ref_commercial, ref_coordonnee, date_insertion, unite_mesure, id_piece)
    ''', (new_capteur['ref_commercial'], new_capteur['ref_coordonnee'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), new_capteur['unite_mesure'], new_capteur['id_piece']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Nouveau Capteur enregistré"})



# Route GET pour consulter l'ensemble des mesures 
@app.route('/Mesure', methods=['GET']) 
def get_Mesure():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM Mesure")
    Mesure = c.fetchall()                   # Récupère le résultat de la requête
    conn.close()
    return jsonify([dict(row) for row in Mesure]) 

# Route POST pour ajouter une nouvelle mesure
@app.route('/Mesure', methods=['POST'])
def post_Mesure(): 
    new_mesure = request.json                   #Extraction des données au format JSON
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO Mesure (id, valeur, date_insertion, sn_capteur)
        VALUES (?, ?, ?, ?)
    ''', (new_mesure['id'], new_mesure['valeur'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), new_mesure['sn_capteur']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Nouvelle mesure enregistrée"}), 201 



# Route GET pour consulter l'ensemble des factures 
@app.route('/Facture', methods=['GET'])
def get_Facture():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM Facture")
    Facture = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in Facture])

# Route POST pour ajouter une nouvelle facture
@app.route('/Facture', methods=['POST'])
def post_Facture():
    new_facture = request.json
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO Facture (id, nature, date_facture, montant, valeur_consomee, id_logement)
        VALUES (?, ?, ?, ?, ?)
    ''', new_facture['id'], new_facture['nature'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), new_facture['montant'], new_facture['valeur_consommee'], new_facture['id_logement'])
    conn.commit()
    conn.close()
    return jsonify({"message": "Nouvelle facture enregistrée"}), 201





# 2.2: objectif: répondre à une requête GET tout en créant un camembert dans lequel afficher les données envoyées au client (les factures)


# Route GET pour afficher un camembert représentant la répartitions des factures d'un logement
@app.route('/Facture_PieChart', defaults={'id_logement': None}, methods=['GET'])
@app.route('/Facture_PieChart/<int:id_logement>', methods=['GET'])
def facture_pie_chart(id_logement):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    if id_logement is None:
        c.execute("SELECT nature, SUM(montant) AS total_montant FROM Facture GROUP BY nature")
        title = "Répartiton du montant des factures de tout les logements par nature de facture"
    else:
        c.execute("SELECT nature, SUM(montant) AS total_montant FROM Facture WHERE id_logement = ? GROUP BY nature", (id_logement,))
        title = f"Répartition du montant des factures du logement {id_logement}"

    Facture = c.fetchall()
    conn.close()
    facture_chart = [["nature", "montant"]]
    for facture in Facture:
        facture_chart.append([facture['nature'], facture['total_montant']])

    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Graphique des Factures</title>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
            google.charts.load('current', {'packages':['corechart']});
            google.charts.setOnLoadCallback(drawChart);
            function drawChart(){
                var data = google.visualization.arrayToDataTable({{ data|safe }});
                var options = {
                    title: '{{title}}',
                    is3D: true
                }; 
                var chart = new google.visualization.PieChart(document.getElementById('piechart'))
                chart.draw(data, options);
            }
        </script>
    </head>
    <body>
        <div id="piechart" style="width: 900px; height: 500px;" ></div>
    </body>
    </html>
    """

    return render_template_string(template, data=facture_chart, title=title)



# 2.3: objectif: répondre à une requête GET qui se chargera de récupérer les prévisions météo des 5 jours à venir


# Route GET pour récupérer et afficher les prévisions météo des 5 jours à venir depuis une API REST de météo
@app.route('/meteo', methods=['GET'])
def get_Meteo():
    # Paramètre à changer suivant l'utilisateur ou le lieu dont on veut connaitre la météo
    API_key = 'd662ad910f20403da6f100756240412'
    city = 'Paris'
    avance = 3
    url = f'http://api.weatherapi.com/v1/forecast.json?key={API_key}&q={city}&days={avance}&aqi=yes&alerts=yes'
    # Requête vers l'API météo
    response = requests.get(url)

    if response.status_code == 200:
        # On récupère les données fournies par le serveur au format JSON
        data = response.json()

        forecast = data['forecast']['forecastday']
        location = data['location']['name']
        
        # Préparer les prévisions
        forecast_data = []
        for day in forecast:
            date = day['date']
            temp_max = day['day']['maxtemp_c']
            temp_min = day['day']['mintemp_c']
            condition = day['day']['condition']['text']
            forecast_data.append({'date': date,
                                  'temp_max': temp_max,
                                  'temp_min': temp_min,
                                  'condition': condition})
        
        template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Météo à {{ location }}</title>
        <head>
        <body>
            <h1>Prévision météo à {{ location }}</h1>
            <table border="1">
                <tr>
                    <th>Date</th>
                    <th>Température Max</th>
                    <th>Température Min</th>
                    <th>Condition</th>
                </th>
                {% for day in forecast %}
                <tr>
                    <td>{{ day.date }}</th>
                    <td>{{ day.temp_max }}°C</td>
                    <td>{{ day.temp_min }}°C</td>
                    <td>{{ day.condition }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
        </html>
        """

        return render_template_string(template, location=location, forecast=forecast_data)
    

    else:
        return jsonify({"error": "Impossible de récupérer les données météo"}), 500




if __name__ == '__main__':
    app.run(debug=True)