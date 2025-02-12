import time
from bluepy.btle import Scanner, DefaultDelegate,  Peripheral

def hexa_decimal(hex_data):
    
    hex_data_batt = hex_data[20:22]
    # print(hex_data_batt)
    dec_data_batt = int(hex_data_batt,16)
    print(dec_data_batt,"%")
    
    hex_data_hum = hex_data[28:32]
    # print(hex_data_hum)
    dec_data_hum = int(hex_data_hum,16)/100
    print(dec_data_hum,"%")
    
    hex_data_temp = hex_data[24:28]
    # print(hex_data_temp)
    dec_data_temp = int(hex_data_temp,16)
    bit_sign = (dec_data_temp >> 14) & 1
    temperature = dec_data_temp & ((2**14)-1)
    if bit_sign == 1 :
        temperature = -temperature
    temperature = temperature/100
    print(temperature,"°")
    

    return temperature, dec_data_hum, dec_data_batt


TARGET_MAC_ADDRESSES = [
    "D6:1C:BF:B7:76:62",  
    "D7:EF:13:27:15:29",
    "D6:C6:C7:39:A2:E8"  
]
data = ""
temp = 0
hum = 0 
batt = 0

 # Classe pour gérer les événements de scan
class ScanDelegate(DefaultDelegate):
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print(f"Nouvel appareil détecté : {dev.addr}")
        elif isNewData:
            print(f"Données mises à jour pour : {dev.addr}")
            
       

scanner = Scanner().withDelegate(ScanDelegate())
print("Scan des périphériques Bluetooth...")
devices = scanner.scan(10.0) # scan 10sec      

while True:
    
    for device in devices:
        if device.addr.upper() in TARGET_MAC_ADDRESSES:
            for adtype, description, value in device.getScanData(): 
                
                print(f" ({adtype}) {description} = {value}")
                data = value
                print (value)
                hex_data = value

                temp, hum, batt = hexa_decimal(hex_data)
               

                time.sleep(3)
