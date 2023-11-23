import requests
import subprocess
import creds
from datetime import datetime
from sense_hat import SenseHat

origin = 'Maynooth+Park,Maynooth,Kildare,Ireland'
destination = 'Bray+Promenade,Bray,Wicklow,Ireland'
userPresent = True

sense = SenseHat()
sense.clear()
green = (0, 255, 0)
red = (255,0,0)
blue = (0,0,255)

# array that the difference between actual departure time and desired departure time is passed. The average of the array contents will be added to timeInSeconds and duration in traffic.
averageDelay = []

apiUrl = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={creds.apiKey}&departure_time=now'

while userPresent:
    try:
        pingCheck = subprocess.call(["ping", "192.168.1.10", "-c1", "-W2", "-q"])
        if pingCheck == 0:
            userPresent = True
            print("Successful connection to phone. User is yet to leave")
        else :
            print("No connection. User is on their way to work!")
            userPresent = False
            sense.show_message(f'ON THEIR WAY', text_colour = blue)
            break
        # initializing datetime object as a reference for the current time
        currentDate = datetime.now()
        # using the datetime object functions to convert the current date's time values into seconds
        timeInSeconds = (currentDate.hour * 3600) + (currentDate.minute * 60) + currentDate.second
        response = requests.get(apiUrl)
        data = response.json()

        if data['status'] == 'OK':
            durationInTraffic = data['rows'][0]['elements'][0]['duration_in_traffic']['value']  # in seconds
            estimatedArrivalTimeInSeconds = timeInSeconds + durationInTraffic

            # Convert estimated arrival time to a UTC date
            estimatedArrivalDate = datetime.utcfromtimestamp(estimatedArrivalTimeInSeconds)

            # Extract hours and minutes in UTC format
            hoursUTC = estimatedArrivalDate.hour
            minutesUTC = estimatedArrivalDate.minute

            print(f'Estimated time of arrival: {hoursUTC}:{minutesUTC:02}')

            # if statement to check arrival time and use color appropriately
            if hoursUTC <= 20 and minutesUTC <= 42:
                sense.show_message(f'ETA: {hoursUTC}:{minutesUTC:02}', text_colour = green)
                print(f'ETA: {hoursUTC}:{minutesUTC:02}')
                print(f'GREEN')
            else:
                sense.show_message(f'ETA:{hoursUTC}:{minutesUTC:02}', text_colour = red)
                print(f'ETA: {hoursUTC}:{minutesUTC:02}')
                print(f'RED!!!')
        else:
            print('Unable to retrieve distance matrix. Check your origin, destination, and API key.')
    except Exception as error:
        print('Error fetching distance matrix:', str(error))

