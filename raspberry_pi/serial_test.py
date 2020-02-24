import wiringpi
import time

wiringpi.wiringPiSetup()
serial = wiringpi.serialOpen('/dev/ttyS0', 9600)

while True:
    wiringpi.serialPuts(serial, 'hello world!')
    print("sent")
    time.sleep(1)
