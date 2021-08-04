import signal
import sys
import time

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import openBCIStream
from threading_class import *


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


## Keyboard Interrupt handler
def keyboardInterrupt_handler(signum, frame):
    print("  key board interrupt received...")
    print("----------------Recording stopped------------------------")
    raise ServiceExit


def main():
    print("[STARTING] stream is starting..")

    # Socket-Client Handleer -- Implemented via a thread class(definition in threading_class.py)
    clients = []
    socketThread = SocketHandler(clients)
    socketThread.daemon = True
    socketThread.start()
    ecg = []  ## List to store stream of ECG data from device
    n = 250  ## Sampling frequency of OpenBCI-Cyton board

    try:
        signal.signal(signal.SIGINT, keyboardInterrupt_handler)
        cytonBoard = openBCIStream.CytonBoard("/dev/ttyUSB0")

        # Stream data from board using Brainflow API (definition in openBCIStream.py)
        cytonBoard.start_stream()

        ## Plot configurations
        plt.style.use("ggplot")
        fig = plt.figure(figsize=(15, 6))
        move_figure(fig, 2300, 0)
        ax = fig.add_subplot()
        fig.show()

        plt.title(
            "Live ECG Stream on OpenBCI-Cyton", fontsize=15,
        )
        plt.ylabel("Voltage in millivolts", fontsize=15)
        plt.xlabel(
            "\nData source: www.pareeknikhil.medium.com | " "Author: @pareeknikhil",
            fontsize=10,
        )

        ##  Streaming service starts
        while True:

            df_ecg = cytonBoard.poll(250)  ## Polling for 250 samples
            ecg.extend(
                df_ecg.iloc[:, 0].values
            )  ## extracting ECG values and appending it into list

            ## Making the plot dynamic with autoscaling and x-axis shifter
            plt.autoscale(enable=True, axis="y", tight=True)
            ax.plot(ecg, color="r")
            fig.canvas.draw()
            ax.set_xlim(left=n - 250, right=n)
            n = n + 250

            time.sleep(1)  ## Updating the window in every one second
        plt.show()

        ## Stop stream from the device
        cytonBoard.stop_stream()

    except ServiceExit:
        cytonBoard.stop_stream()
        socketThread.shutdown_flag.set()
        print("[CLOSED] server closed..")
        sys.exit()


if __name__ == "__main__":
    main()
