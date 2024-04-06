import serial
import time
from datetime import datetime
import math

def check_serial_connection(port='COM6', baudrate=57600):
    try:
        ser = serial.Serial(port, baudrate)
        ser.close()  
        return True
    except Exception as e:
        return e

def read_arduino(port='COM6', baudrate=57600):
    try:
        ser = serial.Serial(port, baudrate, timeout=5)  # open serial port
        ser.write(b'read_eeprom\n')  # send request

        # read data
        data_bytes = ser.read(1024)  # read 1024 bytes of data
        time.sleep(2)

        # Convert bytes to string
        data_str = data_bytes.decode('ascii')

        # Extract numbers from the string
        data_list = [int(num) for num in data_str.split() if num.isdigit()]

        return data_list
    except Exception as e:
        return e

def ff(x):
    print(x)
    if int(x) == 0:
        return 0
    return int(22.75*math.exp(0.0021*x))

def process_arduino_data(data_list):
    for i in range(len(data_list)):
        data_list[i] = ff(data_list[i])
    re = {}
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    re[date] = []
    i = 0
    while i + 1 <= len(data_list) - 1:
        if data_list[i] != 0 and data_list[i+1] != 0:
            re[date].append([min(data_list[i],data_list[i+1]),max(data_list[i],data_list[i+1])])
        i += 2
    return re


