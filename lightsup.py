import requests
import threading, time
from dotenv import load_dotenv
import os
from scapy.all import ARP, Ether, srp

# Get the API key and IP address for our route.
load_dotenv()
API_USER_KEY = os.getenv("API_USER_KEY")
BRIDGE_IP = os.getenv("BRIDGE_IP")
TARGET_MAC_ADDRESS = os.getenv("TARGET_MAC_ADDRESS")
WAIT_TIME_SECONDS = os.getenv("WAIT_TIME_SECONDS")

# Set up basic route and headers for the API calls.
api_route = "http://" + str(BRIDGE_IP) + "/api/" + str(API_USER_KEY)
headers = {"content-type": "application/json", "cache-control": "no-cache"}

# Default device connected as True as user is probably already on the network
device_already_connected = True


def toggleLightState(state):
    payload = '{"on":' + state + "}"
    toggleRequest = requests.put(api_route + "/groups/1/action", data=payload)
    print(toggleRequest.status_code)


# Main function that scans the network for the target device and will toggle lights on/off
def scanner():
    global device_already_connected
    # Address range for local network
    target_ip = "192.168.1.1/24"
    arp = ARP(pdst=target_ip)

    # Target our target mac address
    ether = Ether(dst=TARGET_MAC_ADDRESS)
    packet = ether / arp

    # scan for mac address on network
    result = srp(packet, timeout=5, verbose=0)[0]

    # If we have a result the target device is connected
    if len(result) > 0:
        print("Device Connceted")
        # If the device is already connected, do nothing. Stops lights coming on during night or if they are manually turned off.
        if device_already_connected == True:
            return
        # If the device is not already connected then set connected True and turn on the lights
        else:
            device_already_connected = True
            toggleLightState("true")
    else:
        print("Device Not Connected")
        # If the device was not already connected do nothing.
        if device_already_connected == False:
            return
        # If the device has just disconnected then turn off the lights and set device connected False
        else:
            device_already_connected = False
            toggleLightState("false")


# Set up a thread on a timer to run the script every X seconds
ticker = threading.Event()
while not ticker.wait(int(WAIT_TIME_SECONDS)):
    scanner()