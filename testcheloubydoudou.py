import time
from peewee import *
import datetime

from bluepy.btle import Scanner, DefaultDelegate
from data_analyser import hexa_decimal

TARGET_MAC_ADDRESSES = [
    "D6:1C:BF:B7:76:62",
    "D7:EF:13:27:15:29",
    "D6:C6:C7:39:A2:E8"
]
# Configuration de la base de données (comme avant)
db = MySQLDatabase(
    'weather',
    user='admin',
    password='admin',
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

# Classe pour gérer les événements de scan
class ScanDelegate(DefaultDelegate):
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print(f"Nouvel appareil détecté : {dev.addr}")
        elif isNewData:
            print(f"Données mises à jour pour : {dev.addr}")


scanner = Scanner().withDelegate(ScanDelegate())
print("Scan des périphériques Bluetooth...")
devices = scanner.scan(10.0)  # Scanner pendant 10 secondes

while True:
    
    for device in devices:
        if device.addr.upper() in TARGET_MAC_ADDRESSES:
            nom = "Capteur_" + device.addr[-2:]  # Nom basé sur l'adresse MAC
            adresse_mac = device.addr
            temperature = False
            humidite = False
            batterie = False   
            
            for adtype, description, value in device.getScanData():
                # Filtrer uniquement les données pertinentes
                if description == "16b Service Data" and value.startswith("ffcb"):  # Vérifier le type et le préfixe
                    print(f" ({adtype}) {description} = {value}")
                    print(value)
                    print(value)
                    # Appeler la fonction pour traiter les données
                    temperature, humidite, batterie = hexa_decimal(value)
                    # Insérer les données dans la base
                    Capteur.create(
                        nom=nom,
                        adresse_mac=adresse_mac,
                        temperature=temperature,
                        humidite=humidite,
                        batterie=batterie
                    )
                    
                    
                    # Afficher les résultats
                    print(f"Température : {temp} °C, Humidité : {hum} %, Batterie : {batt} %")
                    print("-" * 50)
                    # Pause de 3 secondes avant le prochain traitement
                    time.sleep(3)
