from bluepy.btle import Scanner
scanner = Scanner()
print("Begin device scan")
while True:
    devices = scanner.scan(timeout=3.0)
    for device in devices:
        print(
            f"Device found {device.addr} ({device.addrType}), "
            f"RSSI={device.rssi} dB"
        )
        for adtype, description, value in device.getScanData():
            print(f"  ({adtype}) {description} = {value}")