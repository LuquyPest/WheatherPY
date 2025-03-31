from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from BDD import *
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/sensor", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )


# # Route pour récupérer les données des capteurs
# @app.get("/sensors")
# def get_sensors():
#     sensors = Sensor.select()
#     return [
#         {
#             "mac": sensor.mac,
#             "temp": sensor.temp,
#             "hum": sensor.hum,
#             "batt": sensor.batt,
#             "heurodatage": sensor.heurodatage.strftime("%Y-%m-%d %H:%M:%S"),
#         }
#         for sensor in sensors
#     ]

# # Route pour servir la page HTML
# @app.get("/", response_class=HTMLResponse)
# def home():
#     html_content = """
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>Live Data</title>
#         <script>
#             async function fetchData() {
#                 try {
#                     const response = await fetch('/sensors'); // Appel à la route /sensors
#                     if (!response.ok) {
#                         console.error('Erreur API:', response.status);
#                         return;
#                     }
#                     const data = await response.json(); // Récupération des données JSON
#                     const container = document.getElementById('data-container');
#                     container.innerHTML = ''; // Réinitialisation du conteneur
#                     data.forEach(sensor => {
#                         const div = document.createElement('div');
#                         div.textContent = `Mac: ${sensor.mac}, Temp: ${sensor.temp}, Hum: ${sensor.hum}, Batt: ${sensor.batt}, Time: ${sensor.heurodatage}`;
#                         container.appendChild(div);
#                     });
#                 } catch (error) {
#                     console.error('Erreur de connexion:', error);
#                 }
#             }

#             setInterval(fetchData, 2000);
#             window.onload = fetchData;
#         </script>
#     </head>
#     <body>
#         <h1>Live Sensors Data</h1>
#         <div id="data-container"></div>
#     </body>
#     </html>
#     """
#     return html_content
