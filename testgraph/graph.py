from fastapi import FastAPI
from fastapi.responses import JSONResponse
from peewee import MySQLDatabase, Model, CharField, FloatField, DateTimeField, FloatField

# Connexion à MariaDB
db = MySQLDatabase(
    'bdd_weath', user='root', password='password', host='localhost', port=3306
)

# Modèle Peewee
class Sensor(Model):
    mac = CharField()
    temp = FloatField()
    hum = FloatField()
    batt = FloatField()
    heurodatage = DateTimeField()

    class Meta:
        database = db

# Création de l'application FastAPI
app = FastAPI()

@app.get("/data")
async def get_data():
    """Renvoie les données de la base sous forme JSON"""
    query = Sensor.select().dicts()
    data = list(query)
    return JSONResponse(content=data)
