from microbit import *
import radio

status = "kandidaten"
kandidaten = {}

radio.config(channel=67, length=32)
radio.on()

sleep(100)

def nieuwe_kandidaat(boodschap):
    global status
    global kandidaten
    boodschap = boodschap.split()
    if boodschap[0].startswith("req"):
        nieuwe = boodschap[1]
        if not nieuwe in kandidaten:
            radio.send("welkom %s als %d" % (nieuwe, len(kandidaten)))
            kandidaten[nieuwe] = str(len(kandidaten))
        else:
            display.scroll("dubbel", delay=75);
    display.scroll("... %d ..." % len(kandidaten), wait=False, loop=True)
    return

def zoek_kandidaten():
    global status
    global kandidaten
    display.scroll('wie doeter mee?', delay=75, wait=False, loop=True)
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
