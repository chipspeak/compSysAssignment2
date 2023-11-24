import requests
import subprocess
import creds
import threading
import sys
import os
import subprocess
from datetime import datetime
from sense_hat import SenseHat

# Get the full path of the current script
current_script_path = os.path.abspath(sys.argv[0])

# Set the current working directory to the directory of the current script
os.chdir(os.path.dirname(current_script_path))

# Relative path to the Python script
script_relative_path = "thingspeak-integration.py"

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
        pingCheck = subprocess.call(["ping", "192.168.1.10", "-c1", "-W2", "-q"])
        if pingCheck == 0:
            userPresent = True
            print("Successful connection to phone. User is yet to leave")
        else:
            print("No connection. User is on their way to work!")
            userPresent = False
            sense.show_message('ON THEIR WAY', text_colour=blue)
            break

        currentDate = datetime.now()
        timeInSeconds = (currentDate.hour * 3600) + (currentDate.minute * 60) + currentDate.second
        response = requests.get(apiUrl)
        data = response.json()

        if data['status'] == 'OK':
            durationInTraffic = data['rows'][0]['elements'][0]['duration_in_traffic']['value']
            estimatedArrivalTimeInSeconds = timeInSeconds + durationInTraffic

            estimatedArrivalDate = datetime.utcfromtimestamp(estimatedArrivalTimeInSeconds)
            hoursUTC = estimatedArrivalDate.hour
            minutesUTC = estimatedArrivalDate.minute
            ETA = f'Estimated time of arrival: {hoursUTC}:{minutesUTC:02}'
            print(ETA)
            def pub(ETA):
                subprocess.run(["python", script_relative_path, "mqtt://mqtt3.thingspeak.com:1883", ETA])
            #subprocess.run(["python", "/home/patspi/dev/mqtt/thingspeak-integration.py", "mqtt://mqtt3.thingspeak.com:1883", ETA])
            x = threading.Thread(target=pub, args=(ETA,))
            x.start()
            if hoursUTC <= 20 and minutesUTC <= 42:
                sense.show_message(f'ETA: {hoursUTC}:{minutesUTC:02}', text_colour=green)
                print(f'ETA: {hoursUTC}:{minutesUTC:02}')
                print(f'GREEN')
            else:
                sense.show_message(f'ETA:{hoursUTC}:{minutesUTC:02}', text_colour=red)
                print(f'ETA: {hoursUTC}:{minutesUTC:02}')
                print(f'RED!!!')
        else:
            print('Unable to retrieve distance matrix. Check your origin, destination, and API key.')
    except Exception as error:
        print('Error fetching distance matrix:', str(error))

