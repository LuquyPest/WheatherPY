import datetime
from peewee import *
TARGET_MAC_ADDRESSES = [
    "D6:1C:BF:B7:76:62",
    "D7:EF:13:27:15:29",
    "D6:C6:C7:39:A2:E8"
]
# Connexion sans base spécifique pour pouvoir la créer
db = MySQLDatabase('bdd_weath', user='pi', password='test', host='localhost', port=3306)

class Sensor(Model):
    mac = CharField()
    temp = FloatField()
    hum = FloatField()
    batt = IntegerField()
    heurodatage = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        
class Name(Model):
    name = CharField()
    mac = CharField()
    class Meta:
        database = db
        
class Alerte(Model):
    tempmax = FloatField()
    tempmin = FloatField()
    hummax = IntegerField()
    hummin = IntegerField()
    battmin = IntegerField()
    emailreceiver = CharField()
    class Meta:
        database = db

# Création des tables si elles n'existent pas ne pas com++
db.connect()
db.create_tables([Sensor,Name,Alerte])


def ajouter_noms():
   
    for index, address in enumerate(TARGET_MAC_ADDRESSES, start=1):
        nom = "Capteur" + str(index)
        
        # Vérifier si le capteur avec ce MAC existe déjà dans la base
        if not Name.select().where(Name.mac == address).exists():
            # Si le nom n'existe pas, on l'ajoute
            Name.create(name=nom, mac=address)
        else:
            print(f"Le capteur avec l'adresse MAC {address} existe déjà.")
def ajouter_alertes():
    if Alerte.select().count() == 0:  # Si la table est vide, ajouter des valeurs par défaut
        Alerte.create(
            tempmax=30.0,
            tempmin=0.0,
            hummax=70,
            hummin=20,
            battmin=20,
            emailreceiver="example@example.com"
        )
         
        

def modifier_nom(ancien_nom, nouveau_nom):
    # Modifier le nom dans la base de données
    nom_a_modifier = Nom.get(Nom.nom == ancien_nom)
    nom_a_modifier.nom = nouveau_nom
    nom_a_modifier.save()
    
    


def rajoutdesinformationsdanslabdd (info1,info2,info3,info4):
    Sensor.create(mac=info1, temp=info2, hum=info3, batt=info4)

def afficherlabdd ():
    for sensor in Sensor.select():
        print(sensor.mac,sensor.temp,sensor.hum,sensor.batt,sensor.heurodatage)
# afficherlabdd()
ajouter_noms()
ajouter_alertes()