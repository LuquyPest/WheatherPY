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

# Création des tables si elles n'existent pas ne pas com++
db.connect()
db.create_tables([Sensor])

def rajoutdesinformationsdanslabdd (info1,info2,info3,info4):
    Sensor.create(mac=info1, temp=info2, hum=info3, batt=info4)

def afficherlabdd ():
    for sensor in Sensor.select():
        print(sensor.mac,sensor.temp,sensor.hum,sensor.batt,sensor.heurodatage)
# afficherlabdd()