from microbit import *
import radio
from machine import unique_id
import machine

radio.config(channel=67, length=32)
radio.on()

uniek = str(unique_id())[:6]

radio.send("req " + uniek)
teamNummer = -1

while teamNummer < 0:
    magmee = radio.receive()
    if magmee is None:
        display.scroll("wacht op quiz master", delay=75)
    elif magmee.startswith("welkom "):
        vanalles = magmee.split()
        if vanalles[1] == uniek:
            laatste = vanalles[3]
            teamNummer = int(laatste)
        else:
            display.scroll("ander team %s" % vanalles[1], delay=75)

display.scroll("team %d" % teamNummer, wait=False, loop=True)
eerste = -1
while True:
    boodschap = radio.receive()
    if boodschap is None:
        pass
    elif boodschap.startswith("welkom"):
        pass
    elif boodschap == "ikstelvraag":
        eerste=-1
        display.scroll("?", wait=False, loop=True)
    elif boodschap.startswith("eerste"):
        eerste = int(boodschap.split()[-1])
        if (teamNummer == eerste):
            display.show([Image.HEART, Image.HAPPY, Image.SMILE], wait=False, loop=True)
        else:
            display.show(Image.ALL_CLOCKS, wait=False, loop=True)
    if eerste < 0 and (button_a.was_pressed() or button_b.was_pressed()):
        display.scroll("buzzz", wait=False, loop=True)
        radio.send("buzz %d" % teamNummer)
    sleep(50)
