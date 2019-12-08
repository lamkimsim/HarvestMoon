import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600) 
time.sleep(9)
ser.write(str.encode('00*00c'))
ser.close()
