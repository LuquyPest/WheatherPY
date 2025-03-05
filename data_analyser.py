def hexa_decimal(hex_data):
    
    hex_data_batt = hex_data[20:22]
    # print(hex_data_batt)
    dec_data_batt = int(hex_data_batt,16)
    # print(dec_data_batt)
    
    hex_data_hum = hex_data[28:32]
    # print(hex_data_hum)
    dec_data_hum = int(hex_data_hum,16)/100
    # print(dec_data_hum)
    
    hex_data_temp = hex_data[24:28]
    # print(hex_data_temp)
    dec_data_temp = int(hex_data_temp,16)
    bit_sign = (dec_data_temp >> 14) & 1
    temperature = dec_data_temp & ((2**14)-1)
    if bit_sign == 1 :
        temperature = -temperature
    temperature = temperature/100
    # print(temperature)
    

    return temperature, dec_data_hum, dec_data_batt