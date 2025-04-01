from dataclasses import dataclass
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from BDD import *
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@dataclass
class Mesure:
    batterie: float
    temperature: float
    humidite: float
    horodatage: datetime



@dataclass
class Capteur:
    mac: str
    mesures: list[Mesure]


TARGET_MAC_ADDRESSES = ["D6:1C:BF:B7:76:62", "D7:EF:13:27:15:29", "D6:C6:C7:39:A2:E8"]


@app.get("/sensor", response_class=HTMLResponse)
async def read_item(request: Request):
    capteurs = []
    for address in TARGET_MAC_ADDRESSES:
        capteur_donnees = Sensor.select().where(Sensor.mac == address)
        mesures = []
        for donnee in capteur_donnees:
            # Créer une instance de Mesure à partir des données
            mesure = Mesure(
                batterie=donnee.batt, temperature=donnee.temp, humidite=donnee.hum, horodatage=donnee.heurodatage
            )
            mesures.append(mesure)

        # Créer une instance de Capteur avec les mesures
        capteur = Capteur(mac=address, mesures=mesures)

        capteurs.append(capteur)
    return templates.TemplateResponse(
        request=request, name="index.html", context={"capteurs": capteurs}
    )

    return html_content
