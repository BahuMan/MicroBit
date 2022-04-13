# Add your Python code here. E.g.
from microbit import *
import radio

status = "kandidaten"
kandidaten = {}

radio.config(channel=67, length=16)
radio.on()

sleep(100)

def nieuwe_kandidaat(boodschap):
    global status
    global kandidaten
    if boodschap == "ikke":
        radio.send("jijbent %d" % len(kandidaten))
        kandidaten[len(kandidaten)] = "doetmee"
    display.scroll("Totnu %d kandidaten" % len(kandidaten), wait=False, loop=True)
    return

def zoek_kandidaten():
    global status
    global kandidaten
    display.scroll('wie doeter mee?', wait=False, loop=True)
    while status == "kandidaten":
        boodschap = radio.receive()
        if boodschap is not None:
            nieuwe_kandidaat(boodschap)
        if button_a.was_pressed() or button_b.was_pressed():
            status = "vraag"
        sleep(50)
    return

def stel_vraag():
    global status
    global kandidaten
    radio.send("ikstelvraag")
    display.scroll('vraag...', wait=False, loop=True)
    eerstekandidaat = -1
    while status == "vraag":
        boodschap = radio.receive()
        if boodschap is not None and boodschap.startswith("buzz"):
            if (eerstekandidaat < 0): #zolang geen kandidaat de buzzer heeft geduwd
                buzznr = int(boodschap.split()[-1]) #laatste woord is de kandidaat nr
                eerstekandidaat = buzznr
                radio.send("eerste %d" % eerstekandidaat)
                display.scroll("buzz %d" % eerstekandidaat, wait=False, loop=True)
        if (button_a.was_pressed() or button_b.was_pressed()):
            return
        sleep(50)
    return

zoek_kandidaten()

while True:
    stel_vraag()

