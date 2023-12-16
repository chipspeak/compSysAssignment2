# imports
import BlynkLib
import os
from time import sleep
from dotenv import load_dotenv

# loading contents of .env
load_dotenv('.env')

# retrieving blynkAuth from .env
blynkAuth = os.getenv('blynkAuth')
# initialize Blynk
blynk = BlynkLib.Blynk(blynkAuth)

# register handler for virtual pin V0 write event (not used but was conceived to allow user to dictate start time via phone input)
@blynk.on("V0")
def v3_write_handler(value):
    sleep(.5)

# register handler for virtual pin V1 write event (this is the virtual pin used to display ETA on the users phone in-app)
@blynk.on("V1")
def v3_write_handler(value):
    sleep(.5)

# register handler for virtual pin V2 write event (this is the virtual pin used for automations relating to phone notifications)
@blynk.on("V2")
def v3_write_handler(value): 
    sleep(.5)



