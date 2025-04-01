import time
from BDD import afficherlabdd, rajoutdesinformationsdanslabdd,TARGET_MAC_ADDRESSES
from bluepy.btle import Scanner, DefaultDelegate
from data_analyser import hexa_decimal
from alerte import check_alerts


scanner = Scanner()
print("Scan des périphériques Bluetooth...")

while True:
    
    devices = scanner.scan(0.5)
    for device in devices:
        if device.addr.upper() in TARGET_MAC_ADDRESSES:
            # mac = TARGET_MAC_ADDRESSES[device.addr.upper()]
            for adtype, description, value in device.getScanData():
                # Filtrer uniquement les données pertinentes
                if description == "16b Service Data" and value.startswith("ffcb"):  # Vérifier le type et le préfixe
                    print(f" ({adtype}) {description} = {value}")
                    print(value)
                    temp, hum, batt = hexa_decimal(value)
                    # Afficher les résultats
                    mac = device.addr.upper()
                    name = len(device.addr.upper())
                    print(f"Température : {temp} °C, Humidité : {hum} %, Batterie : {batt} %")
                    rajoutdesinformationsdanslabdd(mac, temp, hum, batt)
                    check_alerts()
                    time.sleep(3)