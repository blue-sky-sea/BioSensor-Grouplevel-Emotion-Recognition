import json
import random
import select
import signal
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

import openBCIStream

## Keyboard interrupt handler
def keyboardInterrupt_handler(signum, frame):
    print("  key board interrupt received...")
    print("----------------Recording stopped------------------------")


def main():
    print("[STARTING] server is starting..")

    try:
        signal.signal(signal.SIGINT, keyboardInterrupt_handler)
        
        ## This cyton board serial port would change based on your OS as well as port being used to Cyton dongle ##
        cytonBoard = openBCIStream.CytonBoard("/dev/ttyUSB0")
        sampling_freq = cytonBoard.sampling_frequency()

        ## Cytin board has a sampling frequency of 250 Hz ##
        sampling_freq = 250

        # Stream data from board
        cytonBoard.start_stream()

        ## Poll the memory until data for 1 minute is obtained ( 60 sec * 250 Hz)
        df = cytonBoard.poll(15000)

        ## Write the collected Raw ECG data into local csv ## 
        df.to_csv("df_ecg_cyton.csv")

        ## Stop the ECG stream from Cyton serial port ##
        cytonBoard.stop_stream()

        print("[CLOSED] Application closed.")
        sys.exit()

    except:
        pass


if __name__ == "__main__":
    main()
