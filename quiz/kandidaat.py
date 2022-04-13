# Add your Python code here. E.g.
from microbit import *
import radio

radio.config(channel=67, length=16)
radio.on()

radio.send("ikke")
sleep(200)
magmee = radio.receive()

if magmee is None:
    while True:
        display.scroll("quizmaster niet gevonden; reset om opnieuw te proberen")
elif not magmee.startswith("jijbent"):
    while True:
        display.scroll("onbekend antwoord; reset om opnieuw te proberen")
else:
    vanalles = magmee.split()
    laatste = vanalles[-1]
    mijnnr = int(laatste)

display.scroll("ik ben nr %d" % mijnnr, wait=False, loop=True)
eerste = -1
while True:
    boodschap = radio.receive()
    if boodschap is None:
        pass
    elif boodschap == "ikstelvraag":
        eerste=-1
        display.scroll("?", wait=False, loop=True)
    elif boodschap.startswith("eerste"):
        eerste = int(boodschap.split()[-1])
        if (mijnnr == eerste):
            display.show([Image.HEART, Image.HAPPY, Image.SMILE], wait=False, loop=True)
        else:
            display.show(Image.ALL_CLOCKS, wait=False, loop=True)
    if eerste < 0 and (button_a.was_pressed() or button_b.was_pressed()):
        display.scroll("buzzz", wait=False, loop=True)
        radio.send("buzz %d" % mijnnr)
    sleep(50)

