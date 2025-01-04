BENSIDHOUM 
Nicolas
EI4
TP E

Projet: Internet of Things
    LOGEMENT ECO-RESPONSABLE




    1. BASE DE DONNÉES

On commence par écrire un fichier sql dans lequel nous donnerons les premiers ordres à notre nouvel base de données.
Tout d'abord, on écrit les ordres de suppressions des tables des entités si celles-ci existent.
Ensuite, on peut implémenter les tables en spécifiant les différents champs, sans oublier:
    - les clés primaires (pour pouvoir identifier chaque instance d'entité)
    - les clés secondaires (pour spécifier l'appartenance d'une entité à une autre)

Pour créer la base données, on procède de la manière suivante:
    - ouvrir un terminal
    - se placer dans le bon répertoire
    - exécuter la commande sqlite3 database.db: 
        ouvre un shell sqlite3 permettant de créer et/ou de manipuler la base de donnée database.db
    - exécuter la commande .read logement.sql:
        exécute séquentiellement les ordres écrits dans le fichier logement.sql 

Après avoir créé la base de données, on la remplit: j'utilise le langage de programmation python et la librairie Flask. (cf remplissage.py)
    - Pour consulter une table de database.db, j'utilise la fonction c.execute(), prenant en argument une chaîne de caractère (la requête sql)
    - Pour écrire dans database.db, je crée d'abord des classes pour pouvoir stocker les données à écrire, et ensuite je crée une route http pour chacune des requête POST à écrire.

Pour exécuter ce code et les codes suivants, je passe par l'environnement virtuel venv, sans lequel je n'arrive pas à faire fonctionner mon code (et plus particulièrement la librairie flask n'est pas reconnue).
Pour l'installer et l'utiliser: 
    - exécuter python3 -m venv .venv
    - exécuter source .venv/bin/activate 
Je peux alors exécuter le code et ouvrir un serveur en local. 
https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

Pour visualiser la base de données, j'ai utilisé le site suivant: https://sqliteviewer.app/



    2. SERVEUR RESTFUL 

Le but de cette partie et de manipuler notre base de données exclusivement avec des requête GET et POST (cf serveur.py). 
Comme précédemment, j'utilise le langage de programmation python et la librairie flask. 
Pour exécuter le code, je passe par lenvironemment virtuel venv (comme précédemment). 

La première étape est de se connecter à notre base de données (database.db).
La seconde est d'écrire les routes http pour chacune des entités à manipuler et chacune des requêtes (GET et POST) à écrire.
Pour cela, j'ai pris comme référence:
    - https://flask-fr.readthedocs.io/quickstart/
    - ChatGPT: donne moi la structure d'une route http en python avec la librairie flask pour une requête GET puis pour une requête POST

Pour le camembert, je crée deux nouvelles routes (pour le total des logements et pour un seul logement) http (GET) pour lire database.db et en faire un graphique camembert.
j'ai pris en référence: 
    - comment afficher un graphique camembert sur un site internet: https://developers-dot-devsite-v2-prod.appspot.com/chart/interactive/docs/gallery/piechart.html
    - Ahmed Aymane Darai Filali (Midosamaa sur Github) et ChatGPT pour comprendre comment traiter les données afin de les utiliser dans la création du graphique et comment créer une page web à partir d'une route http. 

Pour l'intégration API REST de météo, j'utilise l'API suivante: https://www.weatherapi.com/
L'idée est de créer une page web affichant un tablea contenant les prévisions météo des jours à venir. 
Pour cela, on récupère d'abord les données (variable url) puis on les convertit au format JSON. 
On prépare ensuite les données récupérées à être utiliser dans le camembert. 
Enfin, on écrit le code HTML permettant de générer la page web. 

Références: 
    ChatGPT:
        Comment traiter les données récupérées sur l'API WetherAPI pour avoir un tableau sur une page web contenant les données de prévisions météo 
        Comment créer un tableau en HTML 

Il est important de noter que l'API utilisée ne permet d'avoir les prévisions météo que sur 3 jours maximum, donc la variable "avance" vaut au maximum 3. 
Le code fonctionnera toujours si je choisis avance > 3, mais le tableau des prévisions météo restera inchangé. 



    3. HTML/CSS/Javascript 

On crée ici notre site internet (cf mon_site.py). 
Comme précédemment, on utilise les langages de programmation python et HTML en plus de la librairie flask. 
Comme précédemment, pour exécuter le code, j'utilise l'environnement virtuel venv.

On remplit la base de données afin de faire les vérifications.

Tout d'abord, la page de login: on rentre l'id du logement dont on veut afficher les différentes données. 
Ensuite, une fonction se charge de vérifier la validité de l'identifiant (il faut qu'il soit la clé primaire d'un des logements de la base de données et que ce soit un entier) et redirigeant vers la bonne page web (en récupérant l'id saisi par l'utilisateur).
La page principale du site sert essentiellement à vérifier que la redirection et la lecture des données de database.db fonctionne correctement (en vérifiant que les champs adresse, ip et numero_telephone sont corrects).

Références: 
    - les bases des langages web: https://www.w3schools.com/bootstrap/default.asp
    - comment afficher un linechart sur un site internet: https://developers.google.com/chart/interactive/docs/gallery/linechart
    - ChatGPT:
        Remplissage de la base de données (génération des requêtes sql)
        Fonctionnement des hyperliens et des boutons en HTML
        Différences entre l'implémentation d'un bouton et d'un hyperlien 
        Comment lire une donnée saisie sur une page web grâce à flask avec python 
        Comment fonctionne les exceptions en python
        Comment traiter les données récupérées de ma base de données pour créer une page web possédant un line chart 

        