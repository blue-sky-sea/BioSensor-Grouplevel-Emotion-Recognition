import asyncio
import math
import os
import signal
import sys
import time

import pandas as pd
from bleak import BleakClient
from bleak.uuids import uuid16_dict
import matplotlib
#matplotlib.use('Qt5Agg')
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


#import nest_asyncio
#nest_asyncio.apply()


#from threading import Thread

import datetime
from bleak import BleakScanner
MAC = True#FOR MAC

"""
get Polar H10 UUID in MAc OS/MAC Address in windows
"""

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


#import asyncio
#from bleak import BleakClient
#E7:AF:00:96:72:DB: Polar H10 9563FE26
address = "ED9ABF90-07B6-4137-A8FD-E1926DBF8B43"
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

"""
global ecg_session_data
global ecg_session_time
global ecg_session_nowtime"""
ecg_session_data = []
ecg_session_time = []
ecg_session_nowtime = []

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
    #print("data_conv")
    if data[0] == 0x00:
        timestamp = convert_to_unsigned_long(data, 1, 8)
        step = 3
        samples = data[10:]
        offset = 0
        n=0
        while offset < len(samples):
            ecg = convert_array_to_signed_int(samples, offset, step)
            offset += step
            now_time = datetime.datetime.now()

            #print("ecg:",[ecg]," time:",[timestamp]) 
            #print("ecg:",[ecg]," time:",[timestamp],str(now_time)) 
            if(int(ecg)<=5000):
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

def savetocsv(filePath):
    """global ecg_session_data
    global ecg_session_time
    global ecg_session_nowtime"""
    """df_ecg = pd.DataFrame(columns=['timestamp','nowtime','ecg'])
    df_ecg['timestamp']=ecg_session_time
    df_ecg['nowtime']=ecg_session_nowtime
    df_ecg['ecg']=ecg_session_data"""
    df_ecg = pd.DataFrame(columns=['Time','ECG'])
    df_ecg['Time']=ecg_session_nowtime
    df_ecg['ECG']=ecg_session_data
    ## Writing the collected data into a  CSV file on local system ##
    #df_ecg = pd.DataFrame(ecg_session_data)
    #df_ecg = pd.DataFrame(dic)
    #time.sleep(1)
    df_ecg.to_csv(filePath,index=0)
    print("data saved to",filePath)
    if(ecg_session_data!=[]):
        ecg_session_time.clear()
        ecg_session_nowtime.clear()
        ecg_session_data.clear()
        print("---------this section collected success!---------")


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
    
    n = ECG_SAMPLING_FREQ
    
    total_time=0
    t=0
    n=0#section number iter

    NUM=3#total section number
    T=10#every T second record data to csv


    while n<NUM:
        await asyncio.sleep(1)
        print("Collecting data...",
            "total_costtime",total_time,
            "section_time",t,
            "section_number",n)
        t = t+1
        total_time = total_time+1

        #every T second record data to csv
        if(t==T):
            print(t,n)
            t = 0
            
            #global ecg_session_data
            #print(filePath)
            date = str(datetime.datetime.now().strftime("%m-%d"))
            filePath = "./data/"+date+"df_ecg_polar"+str(n)+".csv"
            #print("save data to",filePath)
            #t1 = threading.Thread(target = savetocsv,name = '线程1')
            if(ecg_session_data==[]):
                print("[warning]:data is None so cant save to",filePath)
            else:
                savetocsv(filePath)
                n +=1
            #t1.start()
                #ecg_session_data=[]

            #
    print("total_time:",total_time,"section_number",n)
        
    #plt.show()
    
    
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
                asyncio.ensure_future(run(client, False)),
            ]

            await asyncio.gather(*tasks)
    #except:
    #    pass


if __name__ == "__main__":
    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
