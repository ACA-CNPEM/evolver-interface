# AMOSTRAS 1 | EVOLVER-1 | DIAS 01, 02 E 05 DE 06/2023

import os
import csv
import glob
import json
import numpy as np

from scipy.optimize import curve_fit

ss_map = {'SS1': 15, 'SS2': 14, 'SS3': 11, 'SS4': 10, 'SS5': 7, 'SS6': 6, 'SS7': 3, 'SS8': 2, 'SS9': 13, 'SS10': 12, 'SS11': 9, 'SS12': 8, 'SS13': 5, 'SS14': 4, 'SS15': 1, 'SS16': 0}
n_samples = 5

def sigmoid(x, a, b, c, d):
    return a + (b - a)/(1 + (10**((c-x)*d)))

#create list of log files
""" 
log_files = []
for file in os.listdir():
    if file.startswith('log_'):
        log_files.append(file+'/od_135b_raw.csv')
print(len(log_files))
 """

#import logs table to a list of dictionaries with format {'time': hh:mm,  'SS1': od_ref,  ...,  'SS16': od_ref}
logs_table = []
with open('cal.csv', 'r') as file:
    csv_file =  csv.DictReader(file)
    for row in csv_file:
        logs_table.append(dict(row))
n_vials = len(logs_table[0])
active_ss = list(logs_table[0].keys())
active_ss.remove('time')
#print(active_ss)


#create list of reference od values
od_ref = []
for log in logs_table:
    for ss in active_ss:
        od = log[ss]
        if od not in od_ref and od != '--':
            od_ref.append(od)
od_ref = [float(i) for i in od_ref]
od_ref.sort()
#print(od_ref)


#create list of LED adjusted values
led_sets = []
log0 = glob.glob('*'+logs_table[0]['time']+'*')[0]
with open(log0+'/od_lede_raw.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        led_sets.append(float(row[2]))
n_leds = len(led_sets)

#create dictionary structure
od_data = {
    'n': n_leds,
    'od': od_ref,
    'led': led_sets
}
for ss in active_ss:
    od_data[ss] = {}
    for value in od_data['od']:
        od_data[ss]['{}'.format(value)] = [[] for _ in range(n_leds)]
#print(od_data)


#populate od_data with logged values
for log in logs_table:
    #print(log)
    path = glob.glob('*'+log['time']+'*')[0]
    with open(path+'/od_135b_raw.csv', 'r') as file:
        reader = csv.reader(file)
        i_sample = 0
        i_led = 0
        for row in reader:
            del row[0:2]
            for ss in active_ss:
                value = row[ss_map[ss]]
                if log[ss] != '--':
                    od_data[ss][log[ss]][i_led].append(int(value))
            i_sample += 1
            if i_sample == n_samples:
                i_sample = 0
                i_led += 1

'''       
for ss in active_ss:
    print(ss)
    print(od_data[ss])
    print("----------------------------------")
    print(od_data)
quit()
'''

coefficients = [[] for ss in active_ss]
covariance = [[] for ss in active_ss]
vial_data = [[] for ss in active_ss]
    
median = [[] for ss in active_ss]
std = [[] for ss in active_ss] 
data_dict = []

for i in range(od_data['n']):
    data_dict += [{
        "name": f"cal_od_led_{od_data['led'][i]}",
        "measuredData": od_data['od'],
        "calibrationType": "od",
        "raw": [],
        "fits": [],
    }]
    
for n,ss in enumerate(active_ss):
    for i in range(od_data['n']):
        vial_data[n] += [[od_data[ss][f'{j}'][i] for j in od_data['od']]]
        data_dict[i]['raw'] += [vial_data[n][i]]

    for i,vial in enumerate(vial_data[n]):
        median[n] += [[np.median(data) for data in vial]]
        std[n] += [[np.std(data) for data in vial]]

        param, cov = curve_fit(sigmoid, od_data['od'], median[n][i], p0=[62721, 62721, 0, -1], maxfev=1000000000)
        coefficients[n].append(np.array(param).tolist())
        covariance[n].append(np.array(cov).tolist())

        data_dict[i]['fits'] += [coefficients[n][i]]
    

for i,led in enumerate(od_data['led']):
    json_object = json.dumps(data_dict[i], indent=len(data_dict[i].keys()))

    with open(f"json/cal_od_{round(led)}.json", "w") as file:
        file.write(json_object)