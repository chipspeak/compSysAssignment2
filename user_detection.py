# imports
import subprocess
import logging
import os
from dotenv import load_dotenv

# loading contents from .env
load_dotenv('.env')

# logging config
logging.basicConfig(filename='user_detection.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

# retrieving phone mac address from .env
phone = os.getenv('phone')

# intialising devices array
devices = [{"name":"user's phone", "mac": phone}]

# Returns the list of known devices found on the network
def find_devices():
    # calling the subprocess and piping the local network results to grep
    output = subprocess.check_output("sudo nmap -sn 192.168.1.0/24 | grep MAC", shell=True)
    # initialising empty devices found array
    devices_found=[]
    # for loop iterating through the devices array
    for dev in devices:
        # conditional checking for a match within the loop   
        if dev["mac"].lower() in str(output).lower():
            logging.info(dev["name"] + " device is present")
            # upon match, devices_found array is appended with the matching entry
            devices_found.append(dev)
        else:
            logging.info(dev["name"] + " device is NOT present")
    return(devices_found)