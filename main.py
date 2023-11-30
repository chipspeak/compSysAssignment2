import requests
import subprocess
import creds
import threading
import sys
import os
import subprocess
import logging
import user_detection
import hue_integration
from huesdk import Hue
from datetime import datetime
from sense_hat import SenseHat

logging.basicConfig(filename='user_detection.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

origin = 'Maynooth+Park,Maynooth,Kildare,Ireland'
destination = 'Bray+Promenade,Bray,Wicklow,Ireland'
userPresent = True

# sensehat variables
sense = SenseHat()
sense.clear()
green = (0, 255, 0)
red = (255,0,0)
blue = (0,0,200)

# array that the difference between actual departure time and desired departure time is passed. The average of the array contents will be added to timeInSeconds and duration in traffic.
averageDelay = []

apiUrl = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={creds.apiKey}&departure_time=now'

while userPresent:
    try:
        if user_detection.find_devices():
            userPresent = True
            print("Successful connection to phone. User is yet to leave")
        else:
            print("No connection. User is on their way to work!")
            userPresent = False
            hue_integration.hueBlue()
            sense.show_message('ON THEIR WAY', text_colour=blue)
            hue_integration.hue.off()
            break

        currentDate = datetime.now()
        timeInSeconds = (currentDate.hour * 3600) + (currentDate.minute * 60) + currentDate.second
        response = requests.get(apiUrl)
        data = response.json()

        if data['status'] == 'OK':
            hue_integration.hue.on()
            durationInTraffic = data['rows'][0]['elements'][0]['duration_in_traffic']['value']
            estimatedArrivalTimeInSeconds = timeInSeconds + durationInTraffic

            estimatedArrivalDate = datetime.utcfromtimestamp(estimatedArrivalTimeInSeconds)
            hoursUTC = estimatedArrivalDate.hour
            minutesUTC = estimatedArrivalDate.minute
            ETA = f'Estimated time of arrival: {hoursUTC}:{minutesUTC:02}'

            #call mqtt related functions here

            if hoursUTC <= 11 and minutesUTC <= 32:
                hue_integration.hueGreen()
                sense.show_message(f'ETA: {hoursUTC}:{minutesUTC:02}', text_colour=green)
                print(f'ETA: {hoursUTC}:{minutesUTC:02}')
            else:
                hue_integration.hueRed()
                sense.show_message(f'ETA:{hoursUTC}:{minutesUTC:02}', text_colour=red)
                print(f'ETA: {hoursUTC}:{minutesUTC:02}')
        else:
            print('Unable to retrieve distance matrix. Check your origin, destination, and API key.')
    except Exception as error:
        print('Error fetching distance matrix:', str(error))