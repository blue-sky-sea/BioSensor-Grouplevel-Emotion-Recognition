#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
import traceback
import datetime

import json

date = str(datetime.datetime.now().strftime('%Y-%m-%d'))
path = "data/"
filename = "2021-08-18liuyi0.txt"

def readdata(filepath):
    data_list=[]
    f = open(filepath,"r")
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n').replace(' ','')
        #rint(line)
        line = eval(line)
        #print(line['temperature'])
        #input()
        data_list.append(line)

    return data_list
     
data = readdata(path+filename)
print(data[1])