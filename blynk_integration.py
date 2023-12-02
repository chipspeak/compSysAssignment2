#imports
import BlynkLib
import os
from time import sleep
from dotenv import load_dotenv
from datetime import datetime, time, timedelta

# loading contents of .env
load_dotenv('.env')

# retrieving blynkAuth from .env
blynkAuth = os.getenv('blynkAuth')
# initialize Blynk
blynk = BlynkLib.Blynk(blynkAuth)

'''
@blynk.on("V0")
def read_handler(value):
    blynkTime = int(value[0])
    startTime = datetime.utcfromtimestamp(blynkTime)
    print(f"User start time: {startTime.hour}:{startTime.minute}")
    blynk.run()
    sleep(.5)
'''

# register handler for virtual pin V1 write event
@blynk.on("V0")
def v3_write_handler(value):
    sleep(.5)

# register handler for virtual pin V2 write event
@blynk.on("V1")
def v3_write_handler(value):
    sleep(.5)

# register handler for virtual pin V2 write event
@blynk.on("V2")
def v3_write_handler(value): 
    sleep(.5)



