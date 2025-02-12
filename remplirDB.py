from bluepy.btle import Scanner
from peewee import *
import datetime

# Configuration de la base de données (comme avant)
db = MySQLDatabase(
    'iot_project',
    user='iot_user',
    password='secure_password',
    host='localhost',
    port=3306
)

# Modèle Peewee pour la table capteurs
class Capteur(Model):
    id = AutoField()
    nom = CharField(max_length=50)
    adresse_mac = CharField(max_length=17)
    temperature = FloatField(null=True)
    humidite = FloatField(null=True)
    batterie = IntegerField(null=True)
    horodatage = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        table_name = 'capteurs'

# Connecter à la base de données
db.connect()
db.create_tables([Capteur])

# Scanner les périphériques Bluetooth
scanner = Scanner()
devices = scanner.scan(5.0)  # Scanner pendant 5 secondes

for device in devices:
    if device.addr.upper() in ["D6:1C:BF:B7:76:62", "D7:EF:13:27:15:29", "D6:C6:C7:39:A2:E8"]:
        # Exemple de données fictives (remplace par les vraies données)
        nom = "Capteur_" + device.addr[-2:]  # Nom basé sur l'adresse MAC
        adresse_mac = device.addr
        temperature = 22.5  # Remplace par la température réelle
        humidite = 60.0      # Remplace par l'humidité réelle
        batterie = 80        # Remplace par le niveau de batterie réel

        # Insérer les données dans la base
        Capteur.create(
            nom=nom,
            adresse_mac=adresse_mac,
            temperature=temperature,
            humidite=humidite,
            batterie=batterie
        )
        print(f"Données insérées pour le capteur : {nom}")
