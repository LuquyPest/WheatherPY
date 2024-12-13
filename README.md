Projet WeatherPY :


Challenge 1 :
    Installer le Raspberry Pi ✅
    Branchement ✅
    Flashage de l'image de Raspbian ✅
    Démarrage du Raspberry Pi ✅
    Accès par : 
        Écran (en direct) ✅
        SSH (par un autre PC) ✅
        FTP (proftpd, par un autre PC avec FileZilla) ✅

Challenge 2 :
    Afficher le résultat du scan Bluetooth
    En faisant un script Python
    Avec la librairie bluepy
    Affichez les données brutes (hexadécimales)

    Challenge 3 :
    Afficher le résultat du scan Bluetooth
    Pareil que le challenge précédent
    Mais affichage intelligible des données :
        Température en degrés °
        Taux d'humidité en %
        État de la batterie en % 

Challenge 4 :
    Stocker les données dans une base de
    données
    Sur le Raspberry Pi
    Base de données MySQL (à installer et
    configurer)
    Faire des requêtes SQL ou utiliser peewee

Challenge 5 :
    Afficher les données des capteurs dans une
    page web
    Actualisée (live)
    Aller au plus simple, mais possibilité d'utiliser
    FastAPI
 
Challenge 6 :
    Afficher l'historique des données
    Triées par capteur et par date
    Rafraichie toutes les cinq minutes

Challenge 7 :
    Proposer une interface pour renommer
    chaque capteur

Challenge 8 :
    Afficher la température extérieure donnée par
    la météo
    Opendata :
    https://donneespubliques.meteofrance.fr/?fon
    d=produit&id_produit=90&id_rubrique=32
    Station BORDEAUX-MÉRIGNAC, ID 07510
    Possibilité d'utiliser httpx

Challenge 9 :
    Gérer des alertes
    Seuil de température ou d'humidité
    Envoi par mail de l'alerte
    Paramétrable
    Configuration des seuils
    Fréquence de scrutation
    Destinataires des mails 

Challenge 10 :
    Afficher les données de température et
    humidité dans un graphe
    De préférence actualisé (live)

