
from bluepy.btle import Scanner, DefaultDelegate, Peripheral


# Liste des adresses MAC des capteurs que tu veux surveiller
TARGET_MAC_ADDRESSES = [
    "D6:1C:BF:B7:76:62",  # Remplace par l'adresse MAC de ton capteur
    "D7:EF:13:27:15:29",
    "D6:C6:C7:39:A2:E8"  
]

# Classe pour gérer les événements de scan
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        super().__init__()

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print(f"Nouvel appareil détecté : {dev.addr}")
        elif isNewData:
            print(f"Données mises à jour pour : {dev.addr}")

# connexion aux capteurs
def main():
    # Initialiser le scanner Bluetooth avec un délégué
    scanner = Scanner().withDelegate(ScanDelegate())

    print("Scan des périphériques Bluetooth...")
    devices = scanner.scan(10.0)  # Scanner pendant 10 secondes

    for dev in devices:
        print(f"Appareil détecté : {dev.addr}, RSSI={dev.rssi} dB")

        # Vérifier si l'appareil fait partie des cibles
        if dev.addr.upper() in TARGET_MAC_ADDRESSES:
            print(f"-> Appareil cible trouvé : {dev.addr}")
            # Ici, tu peux ajouter du code pour te connecter au capteur et lire ses données

# lecture des données
def read_sensor_data(mac_address):
    try:
        # Se connecter au périphérique
        print(f"Connexion à {mac_address}...")
        device = Peripheral(mac_address)

        # Lire une caractéristique (remplace "handle" par le handle ou UUID de la caractéristique)
        handle = 0x0012  # Exemple de handle
        data = device.readCharacteristic(handle)
        print(f"Données lues : {data}")

        # Déconnecter le périphérique
        device.disconnect()
    except Exception as e:
        print(f"Erreur lors de la connexion à {mac_address} : {e}")



main()
read_sensor_data("D6:1C:BF:B7:76:62")
read_sensor_data("D7:EF:13:27:15:29")
read_sensor_data("D6:C6:C7:39:A2:E8")

