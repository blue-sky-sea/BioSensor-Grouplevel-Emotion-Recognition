import asyncio
import math
import os
import signal
import sys
import time

import pandas as pd
from bleak import BleakClient
from bleak.uuids import uuid16_dict

import datetime

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

## This is the device MAC ID, please update with your device ID
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
ecg_session_nowtime = []

## Keyboard Interrupt Handler
def keyboardInterrupt_handler(signum, frame):
    print("  key board interrupt received...")
    print("----------------Recording stopped------------------------")


## Bit conversion of the Hexadecimal stream
def data_conv(sender, data):
    #print("test")
    #print("data[0]",data[0],"??")

    if data[0] == 0x00:

        timestamp = convert_to_unsigned_long(data, 1, 8)
        step = 3
        samples = data[10:]
        offset = 0
        #print(offset,"??",len(samples))
        while offset < len(samples):
            ecg = convert_array_to_signed_int(samples, offset, step)
            offset += step
            now_time = datetime.datetime.now()
            print("ecg:",[ecg]," time:",[timestamp],now_time) 
            ecg_session_data.extend([ecg])
            ecg_session_time.extend([timestamp])
            ecg_session_nowtime.extend([str(now_time)])


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

    ## Collecting ECG data for 1 minute/ 60 seconds
    await asyncio.sleep(40)

    """input("break1")
    print("len,",len(ecg_session_time),len(ecg_session_nowtime),len(ecg_session_data))
    input("break2")"""

    df_ecg = pd.DataFrame(columns=['timestamp','nowtime','ecg'])
    df_ecg['timestamp']=ecg_session_time
    df_ecg['nowtime']=ecg_session_nowtime
    df_ecg['ecg']=ecg_session_data
    ## Writing the collected data into a  CSV file on local system ##
    #df_ecg = pd.DataFrame(ecg_session_data)
    #df_ecg = pd.DataFrame(dic)

    date = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    df_ecg.to_csv(date+"df_ecg_polar.csv")



    ## Stop the stream once data is collected
    await client.stop_notify(PMD_DATA)
    print("Stopping ECG data...")
    print("[CLOSED] application closed.")

    sys.exit(0)


async def main():
    #try:
        async with BleakClient(ADDRESS) as client:
            print("create BleakClient successfully")
            signal.signal(signal.SIGINT, keyboardInterrupt_handler)
            tasks = [
                asyncio.ensure_future(run(client, True)),
            ]

            await asyncio.gather(*tasks)
    #except:
    #    pass


if __name__ == "__main__":
    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
