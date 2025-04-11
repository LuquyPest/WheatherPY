from dataclasses import dataclass
from datetime import datetime

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from BDD import *
from temperatureMerignac import temperature_merignac

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

ajouter_noms()
ajouter_alertes()

temperaturem = temperature_merignac()


@dataclass
class Mesure:
    batterie: float
    temperature: float
    humidite: float
    horodatage: datetime


@dataclass
class Capteur:
    mac: str
    name: str
    mesures: list[Mesure]


TARGET_MAC_ADDRESSES = ["D6:1C:BF:B7:76:62", "D7:EF:13:27:15:29", "D6:C6:C7:39:A2:E8"]


def get_first_sensor_name(mac_address):
    capteur = Name.select().where(Name.mac == mac_address).first()
    return capteur.name if capteur else "Unknown"


@app.get("/sensor", response_class=HTMLResponse)
async def read_item(request: Request):
    capteurs = []
    for address in TARGET_MAC_ADDRESSES:
        capteur_donnees = Sensor.select().where(Sensor.mac == address)
        mesures = [
            Mesure(
                batterie=d.batt,
                temperature=d.temp,
                humidite=d.hum,
                horodatage=d.heurodatage,
            )
            for d in capteur_donnees
        ]
        capteur = Capteur(
            mac=address, name=get_first_sensor_name(address), mesures=mesures
        )
        capteurs.append(capteur)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "capteurs": capteurs,
            "alertes": Alerte.select().first(),
            "temperaturem": temperaturem,
        },
    )


@app.get("/alertes", response_class=HTMLResponse)
async def get_alertes_page(request: Request):
    alertes = Alerte.select().first()
    return templates.TemplateResponse(
        request=request, name="alertes.html", context={"alertes": alertes}
    )


@app.post("/alertes")
async def modifier_alertes(
    request: Request,
    tempmax: float = Form(...),
    tempmin: float = Form(...),
    hummax: int = Form(...),
    hummin: int = Form(...),
    battmin: int = Form(...),
    emailreceiver: str = Form(...),
):
    try:
        alerte = Alerte.select().first()
        alerte.tempmax = tempmax
        alerte.tempmin = tempmin
        alerte.hummax = hummax
        alerte.hummin = hummin
        alerte.battmin = battmin
        alerte.emailreceiver = emailreceiver
        alerte.save()

        return RedirectResponse(url="/sensor", status_code=303)

    except DoesNotExist:
        return {"error": "Alerte non trouvée"}


@app.post("/modifier_nom")
async def modifier_nom(
    request: Request, mac: str = Form(...), nouveau_nom: str = Form(...)
):
    try:
        capteur = Name.get(Name.mac == mac)
        capteur.name = nouveau_nom
        capteur.save()
        return RedirectResponse(url="/sensor", status_code=303)

    except DoesNotExist:
        return {"error": "Capteur non trouvé"}
