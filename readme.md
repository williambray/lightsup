# Lights Up

Lights up is a fun script I wrote in a couple of hours to monitor my home network checking if my mobile phone has connected then turning on my Philips Hue lights for me if I've just got home etc.

It saves if the device was already connected to not constantly turn the lights on/off if you have already manually turned the lights off for bed etc.

## How to use

Create a `.env` file with the following values:

```
API_USER_KEY={YOUR_PHILIPS_API_USER}
BRIDGE_IP={IP_ADDRESS_HUE_BRIDGE}
TARGET_MAC_ADDRESS={TARGET_DEVICE_MAC_ADDRESS}
WAIT_TIME_SECONDS=30
```

Run the following command to install any python packages it needs:

```
  $ sudo pip3 install -r requirements.txt
```

Once the packages are installed, run the this command to run it

```
  $ sudo python3 lightsup.py
```

If you want the script to run in the background you can use `nohup`

```
  $ sudo nohup python3 lightsup.py > output.log &
```

**Note** The script needs to be run as `sudo` because of scapy sending packets or something like that.
