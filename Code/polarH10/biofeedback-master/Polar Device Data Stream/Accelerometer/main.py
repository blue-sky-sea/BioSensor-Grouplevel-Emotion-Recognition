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


""" Predefined UUID (Universal Unique Identifier) mapping are based on Heart Rate GATT service Protocol that most
Fitness/Heart Rate device manufacturer follow (Polar H10 in this case) to obtain a specific response input from 
the device acting as an API """

uuid16_dict = {v: k for k, v in uuid16_dict.items()}

## This is the device MAC ID, please update with your device ID
ADDRESS = "E7:AF:00:96:72:DB"

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

## UUID for Request of ACC Stream ##
ACC_WRITE = bytearray(
    [
        0x02,
        0x02,
        0x00,
        0x01,
        0xC8,
        0x00,
        0x01,
        0x01,
        0x10,
        0x00,
        0x02,
        0x01,
        0x08,
        0x00,
    ]
)

## For Plolar H10  sampling frequency ##
ACC_SAMPLING_FREQ = 200


acc_session_data = []
acc_session_time = []


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
    if data[0] == 0x02:
        timestamp = convert_to_unsigned_long(data, 1, 8)
        frame_type = data[9]
        resolution = (frame_type + 1) * 8
        step = math.ceil(resolution / 8.0)
        samples = data[10:]
        offset = 0
        while offset < len(samples):
            x = convert_array_to_signed_int(samples, offset, step)
            offset += step
            y = convert_array_to_signed_int(samples, offset, step)
            offset += step
            z = convert_array_to_signed_int(samples, offset, step)
            offset += step

            acc_session_data.extend([[x, y, z]])
            acc_session_time.extend([timestamp])


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

    await client.write_gatt_char(PMD_CONTROL, ACC_WRITE)

    ## ECG stream started
    await client.start_notify(PMD_DATA, data_conv)

    print("Collecting ECG data...")
    print(acc_session_data)
    ## Plot configurations
    plt.style.use("ggplot")
    fig = plt.figure(figsize=(15, 6))
    move_figure(fig, 2300, 0)
    ax1 = fig.add_subplot(3, 1, 1)
    ax2 = fig.add_subplot(3, 1, 2)
    ax3 = fig.add_subplot(3, 1, 3)
    fig.show()

    fig.suptitle(
        "Live Accelerometer(mg) Stream on Polar-H10", fontsize=15,
    )

    plt.xlabel(
        "\nData source: www.pareeknikhil.medium.com | " "Author: @pareeknikhil",
        fontsize=10,
    )

    n = ACC_SAMPLING_FREQ

    while True:

        ## Collecting ACC data for 1 second
        await asyncio.sleep(1)
        plt.autoscale(enable=True, axis="y", tight=True)
        ax1.plot(acc_session_data, color="r")
        fig.canvas.draw()
        ax1.set_xlim(left=n - 200, right=n)
        ax1.set_ylabel("X axis", fontsize=10)

        ax2.plot(acc_session_data, color="r")
        fig.canvas.draw()
        ax2.set_xlim(left=n - 200, right=n)
        ax2.set_ylabel("Y axis", fontsize=10)

        ax3.plot(acc_session_data, color="r")
        fig.canvas.draw()
        ax3.set_xlim(left=n - 200, right=n)
        ax3.set_ylabel("Z axis", fontsize=10)

        n = n + 200

    plt.show()

    ## Stop the stream once data is collected
    await client.stop_notify(PMD_DATA)
    print("Stopping ECG data...")
    print("[CLOSED] application closed.")

    sys.exit(0)


async def main():
    try:
        async with BleakClient(ADDRESS) as client:
            signal.signal(signal.SIGINT, keyboardInterrupt_handler)
            tasks = [
                asyncio.ensure_future(run(client, True)),
            ]

            await asyncio.gather(*tasks)
    except:
        pass


if __name__ == "__main__":
    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
