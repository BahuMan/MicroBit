# deze lijn zullen we bijna altijd gebruiken omdat we microbit programmeren:
from microbit import *

# globale variable "signaal" houdt bij of we knop aan het indrukken zijn
signaal = False

# globale variable "laatste" houdt 2 getallen bij: wanneer we de knop
# hebben ingedrukt, en wanneer we de knop hebben losgelaten
laatste = [0, 0]

# globale variabele "tempo" duidt aan in milliseconden hoe lang je
# knop maximaal mag indrukken zodat het signaal als "kort" wordt beschouwd
tempo = 300

# globale variabele "pause" duidt aan dat als je 600 milliseconden
# niks doet, is de morse code compleet en zal Micro:Bit ze vertalen
pause = 600

# globale variable "helptime" duidt aan dat als je 5 seconden niks doet,
# dan toont Micro:Bit een help tekstje
helptime = 5000

# in globale variabele "letter" houden we bij welke codes we tot nu toe
# ontvangen hebben, met punten en streepjes (".-")
letter = ""

# deze globale variabele is een dictionary. Als we zoeken op ".-" krijgen we
# als resultaat "a". Super-handig voor vertalingen en coderen!
translations = {".-": "a",
    "-...": "b",
    "-.-.": "c",
    "-..": "d",
    ".": "e",
    "..-.": "f",
    "--.": "g",
    "....": "h",
    "..": "i",
    ".---": "j",
    "-.-": "k",
    ".-..": "l",
    "--": "m",
    "-.": "n",
    "---": "o",
    ".--.": "p",
    "--.-": "q",
    ".-.": "r",
    "...": "s",
    "-": "t",
    "..-": "u",
    "...-": "v",
    ".--": "w",
    "-..-": "x",
    "-.--": "y",
    "--..": "z"
    }

# hier definieren we een functie die een puntje zet
def showDot(x):
    display.set_pixel(x, 4, 5)

# hier definieren we een functie die een streep trekt
def showDash(x):
    display.set_pixel(x, 4, 9)
    display.set_pixel(x, 3, 9)
    display.set_pixel(x, 2, 9)

# hier definieren we een functie die punten en strepen toont
def showMorse(char):
    display.clear()
    i=0
    for bit in char:
        if (bit == "-"):
            showDash(i)
        else:
            showDot(i)
        i+=1
    return

def translate(fullCode):
    if (fullCode in translations):
        display.scroll(translations[fullCode])
    else:
        display.scroll("?")
    return

# deze functie slaat het tijdstip op waarop de button werd ingeduwd
def button_pressed():
    global signaal # duidt aan dat we de globale variable "signaal" willen veranderen
    global laatste # duidt aan dat we de globale variable "laatste" willen veranderen
    signaal = not signaal
    laatste[int(signaal)] = running_time()
    return

# deze functie kijkt hoelang de knop werd ingeduwd en voegt dan een "." of "-"
# toe aan de huidige letter-code
def button_released():
    global signaal
    global laatste
    global letter
    signaal = not signaal
    #kort of lang signaal?
    if ((running_time() - laatste[1]) < tempo):
        letter += "."
    else:
        letter += "-"
    laatste[int(signaal)] = running_time()
    showMorse(letter)
    return

# deze functie wordt elke keer opnieuw opgeroepen als we geen knoppen induwen.
# daardoor kunnen we na een tijdje beslissen om de morse code te vertalen
# of, na een langere tijd, om een help tekst te tonen
def button_nothing():
    global laatste
    global letter
    #bereken hoe lang het geleden is dat de laatste knop werd losgelaten
    not_pressed = running_time() - laatste[0]
    if (len(letter) == 0):
        #als het al heeel lang geleden is, tonen we helptekst:
        if (not_pressed > helptime):
            display.scroll("use button A to tap morse", delay=100)
            laatste[0] = running_time()
    elif (not_pressed > pause):
        #als er een korte pauze was, is de morse-code compleet en vertalen we ze
        translate(letter)
        letter = ""  # letter leegmaken zodat we opnieuw kunnen beginnen
        laatste[0] = running_time()
    return

# nu alle definities achter de rug zijn, begint hier ons "echte" programma:
while True:
    if (button_a.is_pressed() and not signaal):
        button_pressed()
    elif (signaal and not button_a.is_pressed()):
        button_released()
    elif (not signaal and not button_a.is_pressed()):
        button_nothing()
