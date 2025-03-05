import time
import BDD
from bluepy.btle import Scanner, DefaultDelegate
from data_analyser import hexa_decimal

TARGET_MAC_ADDRESSES = [
    "D6:1C:BF:B7:76:62",
    "D7:EF:13:27:15:29",
    "D6:C6:C7:39:A2:E8"
]
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
            for adtype, description, value in device.getScanData():
                # Filtrer uniquement les données pertinentes
                if description == "16b Service Data" and value.startswith("ffcb"):  # Vérifier le type et le préfixe
                    print(f" ({adtype}) {description} = {value}")
                    print(value)
                    temp, hum, batt = hexa_decimal(value)
                    # Afficher les résultats
                    print(f"Température : {temp} °C, Humidité : {hum} %, Batterie : {batt} %")
                    time.sleep(3)
