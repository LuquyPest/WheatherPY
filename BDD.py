import datetime
from peewee import *

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
