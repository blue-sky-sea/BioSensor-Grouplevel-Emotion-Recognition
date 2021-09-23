import heartpy as hp

import matplotlib.pyplot as plt

filepath = "./maturedata/09-23df_ecg_polar5.csv"
headered_data = hp.get_data(filepath, column_name = 'ECG')
timerdata = hp.get_data(filepath, column_name='Time')

data=headered_data
fs = 130.0
working_data, measures = hp.process(data, fs, report_time=True)
filtered = hp.filter_signal(data, cutoff = 0.05, sample_rate = fs, filtertype='notch')

print(measures)
print('breathing rate is: %s Hz' %measures['breathingrate'])
print('pnn50 is: %s ' %measures['pnn50'])
"""plot_obj = hp.plotter(working_data, measures,show=False)
plot_obj.savefig('plot1.jpg')
plot_obj.show()"""
n=len(data)
l=int(n/12)

print(l)
plt.figure()
plt.plot(data[:l])
plt.plot(filtered[0:l], alpha=0.5, label = 'filtered signal')

#visualise in plot of custom size
#plt.figure(figsize=(12,4))
hp.plotter(working_data, measures)

#plt.legend()
plt.show()



#display computed measures
for measure in measures.keys():
    print('%s: %f' %(measure, measures[measure]))


plot_obj = hp.plot_poincare(working_data, measures,show=False)
plot_obj.savefig('plot1.jpg')

