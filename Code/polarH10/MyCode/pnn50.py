##------------------------------------- Polar H10--------------------------------------------------------------------##

#!python -m pip install heartpy
import pandas as pd
import heartpy as hp

#hrdata = hp.get_data('./data/09-13df_ecg_polar2.csv')
hrdata = pd.read_csv(r"./data/09-13df_ecg_polar2.csv")
"""
#load data from column labeles 'hr' in a delimited file with header info
headered_data = hp.get_data('/content/data2.csv', column_name = 'hr')
timerdata = hp.get_data('/content/data2.csv', column_name='timer')

#if you have a datetime-based timer:
hr_data = hp.get_data('/content/data3.csv', column_name = 'hr')
datetime_data = hp.get_data('data3.csv', column_name='datetime')
fs = hp.get_samplerate_datetime(datetime_data, timeformat='%Y-%m-%d %H:%M:%S.%f')
print(fs)
"""

data=hrdata["ECG"].tolist()
#print(data)
#input()
fs = 100.0
working_data, measures = hp.process(data, fs, report_time=True)
print(measures)
print('breathing rate is: %s Hz' %measures['breathingrate'])
print('pnn50 is: %s ' %measures['pnn50'])
hp.plotter(working_data, measures)