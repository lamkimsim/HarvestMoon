import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600) 
time.sleep(1)
ser.write(str.encode('00*00c'))
ser.close()
