#!/usr/bin/env python3
#networkFileRW.py
#Cornell Johnson
#Thursday, April 7, 2024
#Update routers and switches;
#read equipment from a file, write updates & errors to file
#Use a try/except clause to import the JSON module

#Use a try/except clause to import the JSON module
try:
    import json
except ImportError:
    print("Error: JSON module not found.")
#Create file constants for the file names; file constants can be reused
#There are 2 files to read this program: equip_r.txt and equip_s.txt
#There are 2 files to write in this program: updated.txt and errors.txt
# File names
EQUIP_ROUTER_FILE = "equip_r.txt"
EQUIP_SWITCH_FILE = "equip_s.txt"
UPDATED_FILE = "updated.txt"
INVALID_FILE = "invalid.txt"

#Prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

#Function to read equipment data from a JSON file
def read_equipment_file(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

#Function to write data to a JSON file
def write_json_file(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file)
#function to get valid device
def get_valid_device(routers, switches):
    valid_device = False
    while not valid_device:
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device  
        else:
            print("That device is not in the network inventory.")
#function to get valid IP address
def get_valid_ip(invalid_ip_count, invalid_ip_addresses):
    valid_ip = False
    while not valid_ip:
        ip_address = input(NEW_IP)
        octets = ip_address.split('.')
        #print("octets", octets)
        for byte in octets:
            byte = int(byte)
            if byte < 0 or byte > 255:
                invalid_ip_count += 1
                invalid_ip_addresses.append(ip_address)
                print(SORRY)
                break
        else:
            #validIP = True
            return ip_address, invalid_ip_count
            #don't need to return invalidIPAddresses list - it's an object
def main():
    try:
        # Read equipment data from JSON files
        routers = read_equipment_file(EQUIP_ROUTER_FILE)
        switches = read_equipment_file(EQUIP_SWITCH_FILE)

        updated = {}
        invalid_ip_addresses = []
        invalid_ip_count = 0
        devices_updated_count = 0

        print("Network Equipment Inventory\n")
        print("\tequipment name\tIP address")
        for router, ipa in routers.items(): 
            print("\t" + router + "\t\t" + ipa)
        for switch, ipa in switches.items():
            print("\t" + switch + "\t\t" + ipa)

        while True:
            device = get_valid_device(routers, switches)
            
            if device == 'x':
                break
            
            ip_address, invalid_ip_count = get_valid_ip(invalid_ip_count, invalid_ip_addresses)
      
            if 'r' in device:
                routers[device] = ip_address 
            else:
                switches[device] = ip_address

            devices_updated_count += 1
            updated[device] = ip_address

            print(device, "was updated; the new IP address is", ip_address)

        print("\nSummary:")
        print()
        print("Number of devices updated:", devices_updated_count)

        # Write the updated equipment dictionary to a file
        write_json_file(updated, UPDATED_FILE)

        print("Number of invalid addresses attempted:", invalid_ip_count)

        # Write the list of invalid addresses to a file
        with open(INVALID_FILE, 'w') as file:
            for ip in invalid_ip_addresses:
                file.write(ip + '\n')

    except FileNotFoundError:
        print("Error: One or more files not found.")
    except PermissionError:
        print("Error: Permission denied while accessing files.")
    except Exception as e:
        print("An unexpected error occurred:", e)
#top-level scope check
if __name__ == "__main__":
    main()

