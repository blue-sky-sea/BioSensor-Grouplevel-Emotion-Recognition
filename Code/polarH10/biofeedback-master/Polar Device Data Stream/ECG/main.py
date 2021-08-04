import asyncio
import math
import os
import signal
import sys
import time

import pandas as pd
from bleak import BleakClient
from bleak.uuids import uuid16_dict
import matplotlib.pyplot as plt
import matplotlib



#import asyncio
from bleak import BleakScanner
global h10_address
h10_address=""
async def run():
    devices = await BleakScanner.discover()
    for d in devices:
        print(str(d))
        if(": Polar H10 9563FE26" in str(d)):
            global h10_address
            h10_address=str(d).replace(": Polar H10 9563FE26","")
            h10_address.strip(" ")
            print("polar H10 address:##",h10_address,"##")

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
#6E:7E:D6:86:88:41

#import asyncio
from bleak import BleakClient
#E7:AF:00:96:72:DB: Polar H10 9563FE26
address = "E7:AF:00:96:72:DB"
if( h10_address!=""):
    address = h10_address
else:
    pass


""" Predefined UUID (Universal Unique Identifier) mapping are based on Heart Rate GATT service Protocol that most
Fitness/Heart Rate device manufacturer follow (Polar H10 in this case) to obtain a specific response input from 
the device acting as an API """

uuid16_dict = {v: k for k, v in uuid16_dict.items()}
#6D:2B:2D:EC:EC:6A
## This is the device MAC ID, please update with your device ID
#ADDRESS = "E7:AF:00:96:72:DB"
ADDRESS = address

## UUID for model number ##
MODEL_NBR_UUID = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(
    uuid16_dict.get("Model Number String")
)


## UUID for manufacturer name ##
MANUFACTURER_NAME_UUID = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(
    uuid16_dict.get("Manufacturer Name String")
)

## UUID for battery level ##
BATTERY_LEVEL_UUID = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(
    uuid16_dict.get("Battery Level")
)

## UUID for connection establsihment with device ##
PMD_SERVICE = "FB005C80-02E7-F387-1CAD-8ACD2D8DF0C8"

## UUID for Request of stream settings ##
PMD_CONTROL = "FB005C81-02E7-F387-1CAD-8ACD2D8DF0C8"

## UUID for Request of start stream ##
PMD_DATA = "FB005C82-02E7-F387-1CAD-8ACD2D8DF0C8"

## UUID for Request of ECG Stream ##
ECG_WRITE = bytearray([0x02, 0x00, 0x00, 0x01, 0x82, 0x00, 0x01, 0x01, 0x0E, 0x00])

## For Plolar H10  sampling frequency ##
ECG_SAMPLING_FREQ = 130


ecg_session_data = []
ecg_session_time = []


## Positoning/Pinnning the real-time plot window on the screen
def move_figure(f, x, y):
    """Move figure's upper left corner to pixel (x, y)"""
    backend = matplotlib.get_backend()
    if backend == "TkAgg":
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == "WXAgg":
        f.canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK
        # You can also use window.setGeometry
        f.canvas.manager.window.move(x, y)


## Keyboard Interrupt Handler
def keyboardInterrupt_handler(signum, frame):
    print("  key board interrupt received...")
    print("----------------Recording stopped------------------------")


## Bit conversion of the Hexadecimal stream
def data_conv(sender, data):
    if data[0] == 0x00:
        timestamp = convert_to_unsigned_long(data, 1, 8)
        step = 3
        samples = data[10:]
        offset = 0
        while offset < len(samples):
            ecg = convert_array_to_signed_int(samples, offset, step)
            offset += step
            ecg_session_data.extend([ecg])
            ecg_session_time.extend([timestamp])


def convert_array_to_signed_int(data, offset, length):
    return int.from_bytes(
        bytearray(data[offset : offset + length]), byteorder="little", signed=True,
    )


def convert_to_unsigned_long(data, offset, length):
    return int.from_bytes(
        bytearray(data[offset : offset + length]), byteorder="little", signed=False,
    )


## Aynchronous task to start the data stream for ECG ##
async def run(client, debug=False):

    ## Writing chracterstic description to control point for request of UUID (defined above) ##

    await client.is_connected()
    print("---------Device connected--------------")

    model_number = await client.read_gatt_char(MODEL_NBR_UUID)
    print("Model Number: {0}".format("".join(map(chr, model_number))))

    manufacturer_name = await client.read_gatt_char(MANUFACTURER_NAME_UUID)
    print("Manufacturer Name: {0}".format("".join(map(chr, manufacturer_name))))

    battery_level = await client.read_gatt_char(BATTERY_LEVEL_UUID)
    print("Battery Level: {0}%".format(int(battery_level[0])))

    att_read = await client.read_gatt_char(PMD_CONTROL)

    await client.write_gatt_char(PMD_CONTROL, ECG_WRITE)

    ## ECG stream started
    await client.start_notify(PMD_DATA, data_conv)

    print("Collecting ECG data...")
    
    #from winrt import _winrt

    #_winrt.uninit_apartment()

    print("ecg_session_data",ecg_session_data)

    print("use ggplot")

    ## Plot configurations
    plt.style.use("ggplot")
    fig = plt.figure(figsize=(15, 6))
    move_figure(fig, 2300, 0)
    ax = fig.add_subplot()
    fig.show()

    plt.title(
        "Live ECG Stream on Polar-H10", fontsize=15,
    )
    plt.ylabel("Voltage in millivolts", fontsize=15)
    plt.xlabel(
        "\nData source: www.pareeknikhil.medium.com | " "Author: @pareeknikhil",
        fontsize=10,
    )

    n = ECG_SAMPLING_FREQ
    
    while True:

        ## Collecting ECG data for 1 second
        await asyncio.sleep(1)
        plt.autoscale(enable=True, axis="y", tight=True)
        ax.plot(ecg_session_data, color="r")
        fig.canvas.draw()
        ax.set_xlim(left=n - 130, right=n)
        n = n + 130

    plt.show()

    ## Stop the stream once data is collected
    await client.stop_notify(PMD_DATA)
    print("Stopping ECG data...")
    print("[CLOSED] application closed.")

    sys.exit(0)


async def main():
    #try:
        async with BleakClient(ADDRESS) as client:
            signal.signal(signal.SIGINT, keyboardInterrupt_handler)
            tasks = [
                asyncio.ensure_future(run(client, True)),
            ]

            await asyncio.gather(*tasks)
    #except:
     #   pass


if __name__ == "__main__":
    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
