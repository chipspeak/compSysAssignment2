# imports
from huesdk import Hue
import os
from dotenv import load_dotenv

# loading contents of .env
load_dotenv('.env')

# retrieving hueUsername from .env
hueUsername = os.getenv('hueUsername')

# initialising hue bridge via its local ip
hue = Hue(bridge_ip='192.168.1.1', username=hueUsername)
# initialising the lamp 
light = hue.get_light(name="C.C.A Lamp")

# functions to set the light to specific colours
def hueDefault():
    light.set_brightness(100)
    light.set_color(hexa="#F6E7D2")
def hueBlue():
    light.set_brightness(150)
    light.set_color(hexa="#0000FF")
def hueGreen():
    light.set_brightness(150)
    light.set_color(hexa="#008000")
def hueRed():
    light.set_brightness(150)
    light.set_color(hexa="#FF0000")
def hueYellow():
    light.set_brightness(150)
    light.set_color(hexa="#FFFF00")