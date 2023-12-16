# imports
from datetime import datetime, time, timedelta
import os
import json
import firebase_integration
from datetime import datetime, timedelta, time

# Create a time object that will function as our work start time
startTime = time(hour=21, minute=45)

# create a datetime objects for current date and time and then format them for use with json/db
currentDate = datetime.now()
formattedDate = currentDate.strftime("%Y-%m-%d")
journeyStatus = " "
currentTime = datetime.now()
formattedTime = currentTime.strftime("%H:%M")

# function to write the offset to the json file (called in the offsetCalculation function)
def writeToJSON(formattedDate, offsetInSeconds, formattedTime, ETA, workStart, journeyStatus):
    formattedWorkStart = workStart.strftime("%H:%M")
    formattedETA = ETA.strftime("%H:%M")
    date = formattedDate
    # defining the json data
    journeyData = {
        "Date": str(date),
        "offset": str(offsetInSeconds),
        "Departure": str(formattedTime),
        "ETA": str(formattedETA),
        "Start Time": str(formattedWorkStart),
        "Journey Status": str(journeyStatus),
    }
    jsonFilename = 'journey_data.json'

    firebase_integration.push_db(date, formattedTime, formattedETA, formattedWorkStart, journeyStatus)

    # checking for the json file
    if os.path.isfile(jsonFilename):
        try:
            # Read ('r') existing data
            with open(jsonFilename, 'r') as jsonFile:
                existingData = json.load(jsonFile)
        except json.JSONDecodeError:
            # if there is an error, treat it as an empty list
            existingData = []
    else:
        # if the file is empty, we similarly declare an empty list
        existingData = []

    # Update existing data with the new offset from the start of the function
    existingData.append(journeyData)

    # Write ('w') the updated data to the JSON file
    with open(jsonFilename, 'w') as jsonFile:
        json.dump(existingData, jsonFile, indent=2)
    

# function to read the json and calculate the average offset in seconds based on the lists contents
def calculateAverageOffset():
    # declaring the filename
    jsonFilename = 'journey_data.json'
    if os.path.isfile(jsonFilename):
        try:
            # read ('r') existing data without modifying it
            with open(jsonFilename, 'r') as jsonFile:
                existingData = json.load(jsonFile)

            # extract offsets via list comprehension where the values for the offset entry are placed in this new list (using_ rather then camel case to remain distinct from other uses)
            offsets_in_seconds = [float(entry["offset"]) for entry in existingData]

            # calculate the average offset in seconds with a conditional to account for an empty list (using _as camel case used in final variable declaration)
            if offsets_in_seconds:
                average_offset = sum(offsets_in_seconds) / len(offsets_in_seconds)
                return average_offset
            else:
                # 0 is returned if the list is empty
                return 0
        # similarly if an exception is raised 0 is returned
        except json.JSONDecodeError:
            return 0
    else:
        # if there is no file matching the name provided at the start of the function return 0
        return 0

# average offset set as return from calculateAverageOffset function
averageOffset = calculateAverageOffset()

# combine work start and the current date before subtracting the average offset.
# this results in the user being given prompts via lamp and display earlier based on their average offset
workStart = datetime.combine(currentDate, startTime) - timedelta(seconds=averageOffset)

# subtract 10 minutes for optimal arrival time for use in main
within10 = workStart - timedelta(minutes=10)
# subtract 5 minutes for optimal arrival time for use in main
within5 = workStart - timedelta(minutes=5)

# Extract the time from the result and set values to be called in main
optimalArrival = within10.time()
cuttingItClose = within5.time()

# function to calculate the offset based on the final ETA reading and their start time
def offsetCalculation(ETA):
    # as ETA is currently a time object we are converting it to a full datetime object here
    ETA = datetime.combine(currentDate, ETA)
    
    # subtracting ETA from workstart. If a negative result is returned, we know the user is on time, otherwise they are running late
    offset = ETA - workStart
    offsetInSeconds = offset.total_seconds()

    # print statements for debug
    print(f"ETA: {ETA}")
    print(f"workStart: {workStart}")
    print(f"offsetInSeconds: {offsetInSeconds}")
    print(f"average offset: {abs(averageOffset)}")

    '''
    user will arrive within 10 minutes of their start time resulting in the offset being written to json after conversion to positive via abs function
    chained comparison checks that offsetInSeconds is greater/equal to -600 seconds(10 mins) and then checks that it is less than 0 i.e still a negative meaning on time
    journeyStatus variable is then initialised as "Arriving within ten minutes of start time"
    '''
    if -600 <= offsetInSeconds < 0:
        journeyStatus = "Arriving within ten minutes of starting"
        writeToJSON(formattedDate, abs(offsetInSeconds), formattedTime, ETA, workStart, journeyStatus)

    # offsetInSeconds greater than 0 means user is late so a default offset of 15 minutes is written to the json. journey status is set to "Arriving late"
    elif offsetInSeconds > 0:
        journeyStatus = "Arriving late"
        writeToJSON(formattedDate, 900, formattedTime, ETA, workStart, journeyStatus)

    # user is earlier than 10 minutes therefore 0 is written to the json as there is no need for this to affect the average offset. journey status is set to "Arriving early"
    else:
        journeyStatus = "Arriving early"
        writeToJSON(formattedDate, 0, formattedTime, ETA, workStart, journeyStatus)

        


