import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
filepath = "./maturedata/09-23df_ecg_polar1.csv"

#choose 1/12 data 
ecg_df = pd.read_csv(filepath, skiprows=13, header=None)
n=len(ecg_df)
l=int(n/12)
print(ecg_df[1][:l])

#----------------------------------------------------
#get rri (rr_intervals_list) with biosppy lib
#pip install biosppy
#----------------------------------------------------
from biosppy.signals import ecg

ecg_data = ecg.ecg(signal=ecg_df[1][:l], sampling_rate=130., show=True)

(ts, filtered, rpeaks, templates_ts, templates, heart_rate_ts, heart_rate) = ecg_data
# 体動入りECGデータ
(ts, filtered, _, _, _, _, _,) = ecg.ecg(signal=ecg_df[1], sampling_rate=130., show=False)

rpeaks_christov, = ecg.christov_segmenter(filtered, 130.)
rpeaks_engzee, = ecg.engzee_segmenter(filtered, 130.)
rpeaks_gamboa, = ecg.gamboa_segmenter(filtered, 130.)
rpeaks_hamilton, = ecg.hamilton_segmenter(filtered, 130.)
rpeaks_ssf, = ecg.ssf_segmenter(filtered, 130.)
rpeaks_ssf_2000, = ecg.ssf_segmenter(filtered, 130., threshold=2000.)

ts_peaks = ts[rpeaks_christov]
rri = np.diff(ts_peaks) * 1000
print(rri)

#----------------------------------------------------
#get LF,HF using rri dat with hrv-analysis lib
#https://pypi.org/project/hrv-analysis/   can calculate VLF, LH/HF ratio, LFnu, HFnu, Total_Power
#pip install hrv-analysis
#----------------------------------------------------

from hrvanalysis import remove_outliers, remove_ectopic_beats, interpolate_nan_values
from hrvanalysis import get_time_domain_features,get_frequency_domain_features
frequency_domain_features = get_frequency_domain_features(rri)
print(frequency_domain_features)

print("LF/HF",frequency_domain_features['lf']/frequency_domain_features['hf'])
"""
import scipy

spline_func = scipy.interpolate.interp1d(ts_peaks[:-1], rri, kind='cubic')
ts_1sec = np.arange(ts_peaks[0], ts_peaks[-2], 1)
rri_1sec = spline_func(ts_1sec).round(6)"""