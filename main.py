#imports
import requests
import os
import logging
import user_detection
import hue_integration
import blynk_integration
import time_checks
from datetime import time
from time import sleep
from huesdk import Hue
from datetime import datetime
from sense_hat import SenseHat
from dotenv import load_dotenv
import os

# loading contents of .env
load_dotenv('.env')

logging.basicConfig(filename='user_detection.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

# retrieving api key from .env
apiKey = os.getenv('apiKey')

#declarations for use with api call and user checking functionality
origin = 'Maynooth+Park,Maynooth,Kildare,Ireland'
destination = 'Bray+Promenade,Bray,Wicklow,Ireland'
userPresent = True

# sensehat variables
sense = SenseHat()
sense.clear()
green = (0, 255, 0)
red = (255,0,0)
yellow = (255, 255, 0)
blue = (0,0,200)

# array that the difference between actual departure time and desired departure time is passed. The average of the array contents will be added to timeInSeconds and duration in traffic.
averageDelay = []

# api call
apiUrl = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={apiKey}&departure_time=now'

def statusGreen(ETA):
    hue_integration.hueGreen()
    sense.show_message(f'ETA: {ETA.hour}:{ETA.minute:02}', text_colour=green)
    blynk_integration.blynk.virtual_write(2, 0)
    print(f'ETA: {ETA}')

def statusYellow(ETA):
    hue_integration.hueYellow()
    sense.show_message(f'ETA: {ETA.hour}:{ETA.minute:02}', text_colour=yellow)
    blynk_integration.blynk.virtual_write(2, 1)
    print(f'ETA: {ETA}')

def statusRed(ETA):
    hue_integration.hueRed()
    sense.show_message(f'ETA: {ETA.hour}:{ETA.minute:02}', text_colour=red)
    blynk_integration.blynk.virtual_write(2, 2)
    print(f'ETA: {ETA}')

def statusBlue(ETA):
    hue_integration.hueBlue()
    sense.show_message('ON THEIR WAY', text_colour=blue)
    blynk_integration.blynk.virtual_write(2, 3)
    hue_integration.hue.off()
    time_checks.offsetCalculation(ETA)

# while loop which executes upon successful detection of user on local network via mac address check
while userPresent:
    try:
        #variables declarations re current time and then conversion to minutes and hours
        currentDate = datetime.now()
        timeInSeconds = (currentDate.hour * 3600) + (currentDate.minute * 60) + currentDate.second

        #initialising the response and data variables 
        response = requests.get(apiUrl)
        data = response.json()
        
        #core conditional of programme 
        if data['status'] == 'OK':
            blynk_integration.blynk.run()
            blynk_integration.blynk.virtual_write(2, 4)
            hue_integration.hue.on()
            #variables are created and seconds converted to minutes and hours from api
            durationInTraffic = data['rows'][0]['elements'][0]['duration_in_traffic']['value']
            estimatedArrivalTimeInSeconds = timeInSeconds + durationInTraffic
            estimatedArrivalDate = datetime.utcfromtimestamp(estimatedArrivalTimeInSeconds)
            hoursUTC = estimatedArrivalDate.hour
            minutesUTC = estimatedArrivalDate.minute
            ETA = time(hour=hoursUTC, minute=minutesUTC)
            if user_detection.find_devices():
                userPresent = True
                print("Successful connection to phone. User is yet to leave")
                #blynk functions are called and ETA is passed as an argument           
                blynk_integration.blynk.virtual_write(1, f'ETA: {ETA.hour}:{ETA.minute:02}')
                sleep(.5)
                #conditional effecting the colour of lights and sensedisplay
                if ETA <= time_checks.optimalArrival:
                    statusGreen(ETA)
                elif ETA > time_checks.optimalArrival and ETA <= time_checks.cuttingItClose:
                    statusYellow(ETA)
                else:
                    statusRed(ETA)
            # if user is not on network, departure is inferred and sensehat displays message in addition to lamp powering down
            else:
                print("No connection. User is on their way to work!")
                userPresent = False
                statusBlue(ETA)
                break
        else:
            print('Unable to retrieve distance matrix. Check your origin, destination, and API key.')
    except Exception as error:
        print('Error:', str(error))