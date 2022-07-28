from microbit import *
import radio

#accelerometer.set_range(2)
radio.config(channel=54)
radio.on()
display.on()
dx = -1
dy = -1
dz = -1
streng = 200
punten = 0

def error(p):
    display.scroll(p, wait=True, loop=True)
    
def vergelijk():
    global dx, dy, dz, punten
    print("x:{}".format(dx))
    print("y:{}".format(dy))
    print("z:{}".format((dz)))
    if (dx < 0 or dy < 0 or dz < 0):
        error("verkeerde volgorde van radio boodschappen")

    if (dx < streng and dy < streng and dz < streng):
        punten = punten + 1
        dx = dy = dz = -1
        display.scroll(str(punten), wait=False, loop=True)

    
while True:
    msg = radio.receive()
    if msg is None: continue
    msg = msg.split(":")
    if msg[0] == "x":
        dx = abs(accelerometer.get_x() - int(msg[1]))
    elif msg[0] == "y":
        dy = abs(accelerometer.get_y() - int(msg[1]))
    elif msg[0] == "z":
        dz = abs(accelerometer.get_z() - int(msg[1]))
        vergelijk()
    else:
        error("onbekende radio boodschap: " + msg[0])
