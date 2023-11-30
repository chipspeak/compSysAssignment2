# imports
from huesdk import Hue
import os
from dotenv import load_dotenv

# loading contents of .env
load_dotenv('.env')

#retrieving hueUsername from .env
hueUsername = os.getenv('hueUsername')

# initialising hue bridge via its local ip
hue = Hue(bridge_ip='192.168.1.1', username=hueUsername)
# initialising the lamp 
light = hue.get_light(name="C.C.A Lamp")

# functions to set the light to specific colours
def hueBlue():
    light.set_color(hue=43690)
def hueGreen():
    light.set_color(hue=21845)
def hueRed():
    light.set_color(hue=65535)
def hueYellow():
    light.set_color(hue=12177)