import time
import serial

wireless = serial.Serial(port='/dev/ttyAMA0', baudrate=9600)

counter = 0

while True:
    wireless.write("Does this work?".encode('utf-8'))
    time.sleep(1)
