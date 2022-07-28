from microbit import *
import radio

#accelerometer.set_range(2)
radio.config(channel=54)
radio.on()
display.on()
punten = 0
while True:
    if button_a.is_pressed():
        punten = punten + 1
        radio.send("x:{}".format(accelerometer.get_x()))
        radio.send("y:{}".format(accelerometer.get_y()))
        radio.send("z:{}".format(accelerometer.get_z()))
        print("x:{}".format(accelerometer.get_x()))
        print("y:{}".format(accelerometer.get_y()))
        print("z:{}".format(accelerometer.get_z()))
        while button_a.is_pressed():
            display.scroll(punten, wait=False, loop=True)
