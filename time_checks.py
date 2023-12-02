# imports
from datetime import datetime, time, timedelta
import os
import json
from datetime import datetime, timedelta, time


# function to write the offset to the json file
def writeToJSON(offsetInSeconds):
    # define the json data
    offsetData = {
        "offset": str(offsetInSeconds),
    }
    jsonFilename = 'offset_data.json'

    # check for the json file
    if os.path.isfile(jsonFilename):
        try:
            # Read ('r') existing data
            with open(jsonFilename, 'r') as jsonFile:
                existing_data = json.load(jsonFile)
        except json.JSONDecodeError:
            # if there is an error, treat it as an empty list
            existing_data = []
    else:
        # if the file is empty, we similarly declare an empty list
        existing_data = []

    # Update existing data with the new offset from the start of the function
    existing_data.append(offsetData)

    # Write ('w') the updated data to the JSON file
    with open(jsonFilename, 'w') as jsonFile:
        json.dump(existing_data, jsonFile)
    

# function to read the json and calculate the average offset in seconds based on the lists contents
def calculateAverageOffset():
    # declaring the filename
    jsonFilename = 'offset_data.json'
    if os.path.isfile(jsonFilename):
        try:
            # read ('r') existing data without modifying it
            with open(jsonFilename, 'r') as jsonFile:
                existing_data = json.load(jsonFile)

            # extract offsets via list comprehension where the values for the offset entry are placed in this new list
            offsets_in_seconds = [float(entry["offset"]) for entry in existing_data]

            # calculate the average offset in seconds with a conditional to account for an empty list
            if offsets_in_seconds:
                average_offset = sum(offsets_in_seconds) / len(offsets_in_seconds)
                return average_offset
            else:
            # none is returned if the list is empty
                return None
        # similarly if an exception is raised none is returned
        except json.JSONDecodeError:
            return None  
    else:
        # if there is no file matching the name provided at the start of the function return none
        return None 


# Create a time object
startTime = time(hour=20, minute=55)

# create a datetime object for the current date
currentDate = datetime.now().date()

averageOffset = calculateAverageOffset()

# combine the above
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
    print(f"average offset: {averageOffset}")

    # user will arrive within 10 minutes of their start time resulting in the offset being written to json after conversion to positive via abs function
    # chained comparison checks that offsetInSeconds is greater/equal to 600 seconds(10 mins) and then checks that it is less than 0 i.e still a negative meaning on time
    if -600 <= offsetInSeconds < 0:
        writeToJSON(abs(offsetInSeconds))
        
    # offsetInSeconds greater than 0 means user is late so a default offset of 15 minutes is written to the json
    elif offsetInSeconds > 0:
        writeToJSON(900)
    # user is earlier than 10 minutes therefore 0 is written to the json as there is no need for this to affect the average offset
    else:
        writeToJSON(0)

        


