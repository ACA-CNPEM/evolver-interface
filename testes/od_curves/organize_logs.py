import os
import csv
import numpy as np
import matplotlib.pyplot as plt


ss2channel = [15,14,11,10,7,6,3,2,13,12,9,8,5,4,1,0]


def organize(name):
    columns = []
    for i in range(16):
            columns += [f'SS{i+1}x', f'SS{i+1}y']

    with open(f'{name}/raw.csv', 'r') as log_file:
        log_reader = csv.reader(log_file, delimiter=',')
        raw_data = [row for row in log_reader]
        
    x = []
    y = []
    sum = [0 for i in range(16)]

    p = 0
    for line in raw_data:
        if line[1] == 'od_lede':
            line = line[2:]
            x += [[float(line[ss2channel[i]]) for i in ss2channel]]
                
        else:
            line = line[2:]
                
            if(p < 4):
                sum = [sum[i]+float(line[ss2channel[i]]) for i in range(16)]
                p += 1
                
            else:
                sum = [sum[i]+float(line[ss2channel[i]]) for i in range(16)]
                y += [[sum[i]/5 for i in range(16)]]
                sum = [0 for i in range(16)]
                p = 0

    with open(f'{name}/organized.csv', 'a') as log_file:
        log_writer = csv.writer(log_file, delimiter=';')
        lines = []

        for i in range(len(x)):
            line = []

            for j in range(16):   
                line += [x[i][j]]
                line += [y[i][j]]
            lines += [line]

        log_writer.writerow(columns)
        log_writer.writerows(lines)
    
    return x,y

    
        

def plot(name):
    x = []
    y = []

    if not os.path.isfile(f'{name}/organized.csv'):
        x,y = organize(name)

    else:
        with open(f'{name}/organized.csv', 'r') as log_file:
            log_reader = csv.reader(log_file, delimiter=';')
            raw_data = [row for row in log_reader]

        for row in raw_data[1:]:
            x_data = []
            y_data = []

            for i,item in enumerate(row):
                item = int(float(item))

                if i%2 == 0:
                    x_data += [item]
                else:
                    y_data += [item]
            
            x += [x_data]
            y += [y_data]

    x_data = []
    y_data = []
    
    for i in range(8):
        x_data = [x_line[i] for x_line in x]
        y_data = [y_line[i] for y_line in y]
        plt.plot(x_data, y_data, label=f'SS{i+1}')

    plt.title(f"{name.split('/')[1]}")
    plt.xlabel('LED emission (AD)')
    plt.ylabel('PT detector (AD)')
    plt.legend()

    plt.savefig(f'{name}/all.png')
    plt.show()

    for i in range(8):
        x_data = [x_line[i] for x_line in x]
        y_data = [y_line[i] for y_line in y]

        plt.plot(x_data, y_data)
        plt.title(f"SS{i+1}")
        plt.xlabel('LED emission (AD)')
        plt.ylabel('PT detector (AD)')

        plt.savefig(f'{name}/SSs/SS{i}.png')
        plt.show()
    
    
    


if __name__ == "__main__":
    log_path = 'logs/log_05-05-23_09:01:01'

    if not os.path.exists(f'{log_path}/SSs'):
        os.makedirs(f'{log_path}/SSs')

    plot(log_path)
