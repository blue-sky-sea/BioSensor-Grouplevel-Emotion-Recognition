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


##---------------------------------------------------
#get attention meditation and A-M  by AF7 and TP9
##---------------------------------------------------
def get_A_M(df):
    df = df[['RAW_AF7','RAW_TP9']]
    df.dropna(axis=0, how='any', inplace=True)
    # 因为删除了几行数据,所以index的序列不再连续,需要重新reindex
    df.reset_index(drop=True, inplace=True) 
    print(df)
    
    headset = MuseMonitor(debug=True)
    atts = []
    meds = []
    ams = []
    for i in tqdm(range(len(df))):
        AF7, TP9 = df.iloc[i]
        
        headset._eeg_handler(AF7=AF7, TP9=0)
        attention = headset.attention.value
        meditation = headset.meditation.value
        atts += [attention]
        meds += [meditation]
        ams += [attention-meditation]
        #print(attention)
        #print(meditation)
    return atts,meds,ams
    


def eeg_intercept():
    input_filepath = "."+data_dir_name+input_dir+"/" #/cuidenwen-09-24/rawdata/
    concat_eeg_df = read_concat_csv(filepath=input_filepath,
                                 file_name=eeg_file_name,
                                 n=eeg_file_num,
                                 file_format=".csv")
    #删除无用特征，然后删除有na的行
    concat_eeg_df = drop_feature(concat_eeg_df)
    concat_eeg_df = drop_na(concat_eeg_df)
    
    concat_eeg_df['TimeStamp'] = pd.to_datetime(concat_eeg_df['TimeStamp'])
    print("concat_ecg_df(dropna and resized)")
    print(concat_eeg_df)
	

    for i in range(len(sr_df)):
		#print(aa.iloc[i])
        starttime = str(sr_df['StartTime'].iloc[i])
        endtime = str(sr_df['EndTime'].iloc[i])
        starttime= date_ + " " + starttime.strip('PM').strip('AM')
        endtime= date_ + " " + endtime.strip('PM').strip('AM')
        
        #starttime - 30s
        #(取最后一分钟数据，计算Attention和Meditation的话，前5秒左右的结果为0)
        starttimeArray = datetime.datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S')
        delta = datetime.timedelta(seconds=120)
        starttime = starttimeArray - delta
        # starttime - 2min
        #because we need to calculate LF/HF(which need ecg data 2minutes before)
        #starttimeArray = datetime.datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S')
        #delta = datetime.timedelta(minutes=2)
        #starttime = starttimeArray - delta
        
        print(starttime,endtime)
        
         
        data = concat_eeg_df[(concat_eeg_df['TimeStamp'] >=starttime) & (concat_eeg_df['TimeStamp'] <= endtime)]
        #print( data)

		##------------------------------------
		##save data to csv
		##------------------------------------
        save_filePath = data_path + output_dir1 +"/"+ "eeg"+str(i)+".csv"
        savecsv(save_filePath,data)
        #int(type(eeg_rawdata['TimeStamp'][0]),eeg_rawdata['TimeStamp'][0])
        
        
def get_am_from_eeg(filepath):
    #print(filepath)
    df = readcsv(filepath)
    #print(df)
    atts,meds,ams = get_A_M(df)
    #print(atts,meds,ams)
    
    #print(len(df),len(atts),len(ams))
    df['Attention']=atts
    df['Meditation']=meds
    df['A_M']=ams
    #print(df)
    #pass
    return df
###--------------------------------------------------------------------------------
#判断一下有没有重复秒,如果有，删除
#保证60s的数据每一秒有一行，一共60行
###--------------------------------------------------------------------------------
def delete_sametime_row(totaltime,data):
    #判断一下有没有重复秒,如果有，删除
    if(len(data)>totaltime):
        print(save_filePath," has duplicated time data row",len(data))
        stamps=[]
        for j in range(len(data['TimeStamp'])):
            stamp = data['TimeStamp'].iloc[j]
            stamp = stamp.split('.')[0]
            print(stamp)
            time = datetime.datetime.strptime(stamp, '%Y-%m-%d %H:%M:%S')
            stamps.append(time)
        #print(stamps)
        data['Time'] = stamps
        #print(data['Time'])
        #input("transfer")]

        ##--------------------------------------------------------------------------------
        ##create new Time columns 2021-09-27 11:18:58 to delete duplicate row
        ##in order to get 1 second 1row data
        my_subset = ['Time']
        data = data.drop_duplicates(subset=my_subset)
        #因为删除了几行数据,所以index的序列不再连续,需要重新reindex
        data.reset_index(drop=True, inplace=True)

        # 丢弃特征 drop Time columns to get data 
        data.drop( my_subset, axis=1, inplace=True)
        #print(data)
        #input("Dlete duplicated!")
        ##--------------------------------------------------------------------------------
    return data

def am_calculate():
   for i in range(len(sr_df)):
        filepath = data_path + output_dir1 +"/"+ "eeg"+str(i)+".csv"
        df = get_am_from_eeg(filepath)

        #concat --》 1m
        starttime = str(sr_df['StartTime'].iloc[i])
        endtime = str(sr_df['EndTime'].iloc[i])
        starttime= date_ + " " + starttime.strip('PM').strip('AM')
        endtime= date_ + " " + endtime.strip('PM').strip('AM')
        print(starttime,endtime)
        data = df[(df['TimeStamp'] >=starttime) & (df['TimeStamp'] <= endtime)]

        save_filePath = data_path + output_dir2 +"/"+ "eeg"+str(i)+".csv"
        savecsv(save_filePath,data)


        #delete duplicated
        #移除重复项
        #data2.duplicated()
        stamps=[]
        for j in range(len(data['TimeStamp'])):
            stamp = data['TimeStamp'].iloc[j]
            stamp = stamp.split('.')[0]
            #print(stamp)
            time = datetime.datetime.strptime(stamp, '%Y-%m-%d %H:%M:%S')
            stamps.append(time)
        data['Time'] = stamps

        my_subset = [ 'Attention', 'Meditation','A_M','Time']
        data = data.drop_duplicates(subset=my_subset)
        data.reset_index(drop=True, inplace=True)


        #drop Time column
        to_drop = ['Time']
        data = data.drop_duplicates(subset=to_drop)
        data.drop(to_drop,axis=1, inplace=True)
        #因为删除了几行数据,所以index的序列不再连续,需要重新reindex
        data.reset_index(drop=True, inplace=True)


        #totaltime=60
        #data = delete_sametime_row(totaltime,data)


        #save to csv
        save_filePath = data_path + output_dir2 +"/"+ "am"+str(i)+".csv"
        savecsv(save_filePath,data)


if __name__=='__main__':
    #intercept every section to 3minutes 
    #save to save_filePath = data_path + output_dir1 +"/"+ "ecg"+str(i)+".csv"
    eeg_intercept()
    
    #for circle to calculate attetntion,meditation,A-M
    #save data to save_filePath = data_path + output_dir2 +"/"+ "ak"+str(i)+".csv"
    am_calculate()

