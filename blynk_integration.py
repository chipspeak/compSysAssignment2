#imports
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

# register handler for virtual pin V0 write event
@blynk.on("V0")
def v3_write_handler(value):
    buttonValue=value[0]
    print(f'Current button value: {buttonValue}')
    blynk.run()
    blynk.virtual_write(1, sys.argv[1]) 
    sleep(.5)