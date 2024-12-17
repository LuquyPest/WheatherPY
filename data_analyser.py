def hexa_decimal(hex_data):
    data = bytes.fromhex(hex_data)

    batt_percentage = data[19]
    batt = batt_percentage * 100 // 0xFF
    print(f"Batterie : {batt} %")

    temp_deg = (data[21] << 8) | data[22]
    temp = temp_deg / 100.0
    print(f"Temp : {temp:.2f} °C")

    hum_percentage = (data[23] << 8) | data[24]
    hum = hum_percentage / 100.0
    print(f"Hum : {hum:.2f} %")

    return temp, hum, batt

hex_data = "030852540201061316FFCB10390102012345670004FFFFFFFF000000"

temp, hum, batte = hexa_decimal(hex_data)