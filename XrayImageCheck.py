#!python3

import os
import cv2
from datetime import date
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm


today = date.today().strftime('%Y%m%d')

directories = [os.path.join('\\\\10.1.230.172\\xray1',today),
               os.path.join('\\\\10.1.230.173\\xray2',today),
               os.path.join('\\\\10.1.230.174\\Images',today),
               'C:\\Users\\Dylan Vanitine\\Desktop\\xray test'
               ]
print(directories[0])

def get_files(directory):
    filepaths=[]
    for root,folders,files in os.walk(directory):
        for filename in files:
            if os.path.splitext(filename)[1]=='.jpg':
                filepath = os.path.join(root,filename)
                filepaths.append(filepath)
    return filepaths

def check_image(file):
    print(file)
    barcode = os.path.basename(file)[13:23]
    code = os.path.basename(file)[5:9]
    im = cv2.imread(file,0)
    averages = im.mean(axis=0)
    avg = averages.mean()
##    averages = list(averages)
    row = [barcode,code,avg,averages]
    return row

                
if __name__ == '__main__':
    
    images = get_files(directories[1])
    data = []

    for file in images:
        data.append(check_image(file))
    
    df = pd.DataFrame(data,columns=['barcode','code','avg','averages'])
##    df2 = df.groupby('code')['averages'].apply(np.mean)
##    df = df.sort_values('code')
    codes = list(df['code'].unique())
    colors = cm.tab20(np.linspace(0,1,len(codes)))
    for x in range(df.shape[0]):
        c = colors[codes.index(df['code'][x])]
        plt.plot(df['averages'][x],color=c,label=df['code'][x])

##    plt.legend(list(df['code']))
    
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))

    plt.legend(by_label.values(),
               by_label.keys(),
               bbox_to_anchor=(1.05, 1),
               loc='upper left',
               )
    
    plt.tight_layout()
    plt.show()
