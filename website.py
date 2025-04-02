
from dataclasses import dataclass
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi import FastAPI,Form
from BDD import *
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from temperatureMerignac import temperature_merignac

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
ajouter_noms()
ajouter_alertes()

temperature = temperature_merignac()

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

def get_first_sensor_name(mac_address):
    # Rechercher le premier capteur avec une adresse MAC spécifique
    capteur = Name.select().where(Name.mac == mac_address).first()
    if capteur:
        return capteur.name
    else:
        return "Unknown"






TARGET_MAC_ADDRESSES = ["D6:1C:BF:B7:76:62", "D7:EF:13:27:15:29", "D6:C6:C7:39:A2:E8"]

@app.post("/modifier_nom")
async def modifier_nom(request: Request, mac: str = Form(...), nouveau_nom: str = Form(...)):
    try:
        # Trouver l'entrée avec l'adresse MAC spécifiée
        capteur = Name.get(Name.mac == mac)
        
        # Modifier le nom
        capteur.name = nouveau_nom
        capteur.save()

        # Après avoir modifié, rediriger vers la page des capteurs
        return RedirectResponse(url="/sensor", status_code=303)
    
    except DoesNotExist:
        return {"error": "Capteur non trouvé"}
    
@app.post("/alertes")
async def alertes(request: Request, tempmax: float= Form(...), tempmin: float= Form(...), hummax: int= Form(...), hummin: int= Form(...), battmin: int= Form(...), emailreceiver: str= Form(...)):
    try:
        
        alerte=Alerte.select().first()
        
        # Modifier le nom
        alerte.tempmax = tempmax
        alerte.tempmin = tempmin
        alerte.hummax = hummax
        alerte.hummin = hummin
        alerte.battmin = battmin
        alerte.emailreceiver = emailreceiver
        
        
        alerte.save()

        # Après avoir modifié, rediriger vers la page des capteurs
        return RedirectResponse(url="/sensor", status_code=303)
    
    except DoesNotExist:
        return {"error": "Capteur non trouvé"}
    
    
    
    

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
        capteur = Capteur(mac=address,name=get_first_sensor_name(address), mesures=mesures)

        capteurs.append(capteur)
    ajouter_alertes()
    return templates.TemplateResponse(
        request=request, name="index.html", context={"capteurs": capteurs, "alertes": Alerte.select().first(),"temperature": temperature}
    )

    return html_content
