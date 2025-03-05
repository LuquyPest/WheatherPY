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

# Création des tables si elles n'existent pas
db.connect()
db.create_tables([Sensor])


print("good")