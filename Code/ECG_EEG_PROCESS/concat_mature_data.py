# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns

from tqdm import tqdm
import sys
sys.path.append('./')
from src.muse import MuseMonitor
from src.pylive import live_plot


import time
import datetime

##------------------!!!!!!!!!!!----------------------
##Be sure you have run ecg_hrv.py and eeg_am,py
##to preprocess data and save them to /output1
##------------------!!!!!!!!!!!----------------------

##---------------------------------------------------
##------------------IMPORTANT------------------------
##---------------------------------------------------
#You should change data's experiment date and collaborator name
##---------------------------------------------------
date = "09-24"
name = "cuidewen"
eeg_file_num = 1 # the number of your 09-27df_ecg_polar .csv in rawdata
##---------------------------------------------------
##------------------IMPORTANT------------------------
##---------------------------------------------------





##---------------------------------------------------
#Global data/file/path setting(according to date and name)
##---------------------------------------------------
date_ ="2021-"+date
date_stamp = "2021"+date.replace("-","")

data_dir_name = "/"+name+"-"+date #/cuidenwen-09-24
input_dir = "/rawdata"
output_dir1 = "/output"
output_dir2 = "/output1"
output_dir3 = "/output2"

ecg_file_name = date+"df_ecg_polar"  #09-24df_ecg_polar0.csv
eeg_file_name = "museMonitor_"+"2021-"+date+"--" #museMonitor_2021-09-24--0.csv
sr_file_name = name+"-"+date+"SR.csv" #cuidenwen-09-24SR.csv

data_path = "."+data_dir_name
##---------------------------------------------------

##---------------------------------------------------
##read data's info (self-report csv)
print("Read SR csv:",sr_file_name)
sr_df =  pd.read_csv('%s/%s' % (data_path, sr_file_name) )#SR.csv

print(sr_df)
print("-"*50)
##---------------------------------------------------


##---------------------------------------------------
#readcsv function
#read csvs and  concat them into one csv file
##---------------------------------------------------
def readcsv(filepath):
	df = pd.read_csv(filepath)
	return df

def read_concat_csv(filepath,file_name,n,file_format):
	#df = None
	frames = []
	for i in range(n):
		#print(i)
		df = readcsv(filepath+file_name+str(i)+file_format)
		frames.append(df)	
	dataframe = pd.concat(frames)
	return dataframe

def savecsv(filepath,data):
    data.to_csv(filepath,index=0)
    print("saved to ",filepath)
    print("-"*50)  

##---------------------------------------------------
#drop na and useless feature data in df
##---------------------------------------------------
def drop_feature(data):
	df=data
	"""to_drop =['RAW_TP9', 'RAW_AF7', 'RAW_AF8', 'RAW_TP10', 'AUX_RIGHT',
	       'Accelerometer_X', 'Accelerometer_Y', 'Accelerometer_Z', 'Gyro_X',
	       'Gyro_Y', 'Gyro_Z', 'HeadBandOn', 'HSI_TP9', 'HSI_AF7', 'HSI_AF8',
	       'HSI_TP10', 'Battery', 'Elements']"""
	to_drop =['HeadBandOn', 'HSI_TP9', 'HSI_AF7', 'HSI_AF8',
	       'HSI_TP10', 'Battery', 'Elements']
	# 丢弃特征 drop columns
	df.drop(to_drop, axis=1, inplace=True)
	print("feature droped!")
	return df

def drop_na(data):
	df=data
	df.dropna(axis=0, how='any', inplace=True)
	# 因为删除了几行数据,所以index的序列不再连续,需要重新reindex
	df.reset_index(drop=True, inplace=True)
	return df


     
def hrv_am_sr_data_concat():
    
    for i in range(len(sr_df)):
        hrv_filePath = data_path + output_dir2 +"/"+ "rv"+str(i)+".csv"
        am_filePath = data_path + output_dir2 +"/"+ "am"+str(i)+".csv"
        
        hrv_df = readcsv(hrv_filePath)
        am_df = readcsv(am_filePath)
        
        #print(hrv_df)
        #print(am_df)
        df = pd.concat([hrv_df,am_df],axis=1)
        
        #concat sr_df ,too
        #sr_l = sr_df.iloc[i]
        #print(sr_l)
        #df = pd.concat([hrv_df,],axis=1)
        
        print(df)
        
        
        #save df to save_filepath
        save_filepath = data_path + output_dir3 +"/"+ "data"+str(i)+".csv"
        savecsv(save_filepath,df)


if __name__=='__main__':
		
	hrv_am_sr_data_concat()




