from huesdk import Hue
import os
from dotenv import load_dotenv

load_dotenv('.env')

hueUsername = os.getenv('hueUsername')

hue = Hue(bridge_ip='192.168.1.1', username=hueUsername)
light = hue.get_light(name="C.C.A Lamp")

def hueBlue():
    light.set_color(hue=43690)
def hueGreen():
    light.set_color(hue=21845)
def hueRed():
    light.set_color(hue=65535)