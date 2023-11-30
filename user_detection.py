import subprocess
import logging

logging.basicConfig(filename='user_detection.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

devices = [{"name":"pat's phone", "mac":"62:AA:B2:99:A3:C5"}]

# Returns the list of known devices found on the network
def find_devices():
    output = subprocess.check_output("sudo nmap -sn 192.168.1.0/24 | grep MAC", shell=True)
    devices_found=[]
    for dev in devices:   
        if dev["mac"].lower() in str(output).lower():
            logging.info(dev["name"] + " device is present")
            devices_found.append(dev)
        else:
            logging.info(dev["name"] + " device is NOT present")
    return(devices_found)

# Main program (prints the return of arp_scan )
def main():
    print(find_devices())

if __name__ == "__main__":
    main()