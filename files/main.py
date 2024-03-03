#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

import glob
import os
from shutil import move
import copy

from rndflow import job

# Load everything from input package:
globals().update(job.load())
globals().update(job.params())

files = glob.glob('**',recursive = True)

# Or, loop over input packages:
for pkg in job.packages():
    meta = globals().update(pkg.fields) # загрузка переменной "content"
    data = pkg.load() # загрузка массивов "arrayX","arrayY"
    label = pkg.label # загрузка имени пакета "package 1"

package=package.decode('utf-8')
result=dict()

if len(sensor_name)!=1:
    sensor_name=[i for i in range(sensor_name[0],sensor_name[1]+1)]
    
ww=dict.fromkeys(sensor_name,)
for i,line in enumerate(field):
    line=int(line.decode('utf-8').split()[0])
    try:
        sensor_name.index(line)
        ww[line]=i
    except ValueError:
        pass

ww=dict(sorted(ww.items()))

k=0
for name,num in ww.items():
    print(num,name,k)
    # plot graph
    xlabel=['t,sec','f,Hz','t,sec','f,Hz','t,sec','f,Hz']
    ylabel=['Z']*2+['X']*2+['Y']*2
    title=['Signals','Spectrum']*3
    fig = plt.figure(num=k,figsize=(10,8))
    fig.subplots_adjust(hspace=0.8, wspace=0.8)
    X=list()
    Y=list()

    X.extend([np.arange(len(data['results']['signals']['N'][str(num)]['Z']['s'])),data['results']['spectrums']['N'][str(num)]['Z']['f'][0],np.arange(len(data['results']['signals']['N'][str(num)]['Z']['s'])),data['results']['spectrums']['N'][str(num)]['X']['f'][0],
             np.arange(len(data['results']['signals']['N'][str(num)]['Z']['s'])),data['results']['spectrums']['N'][str(num)]['Y']['f'][0]])

    Y.extend([np.array(data['results']['signals']['N'][str(num)]['Z']['s'],dtype=float),data['results']['spectrums']['N'][str(num)]['Z']['A'][0],np.array(data['results']['signals']['N'][str(num)]['X']['s'],dtype=float),data['results']['spectrums']['N'][str(num)]['X']['A'][0],
              np.array(data['results']['signals']['N'][str(num)]['Y']['s'],dtype=float),data['results']['spectrums']['N'][str(num)]['Y']['A'][0]])

    for i in range(1,7):
        ax = fig.add_subplot(3, 2, i)
        ax.plot(X[i-1],Y[i-1])
        plt.title(title[i-1])
        plt.xlabel(xlabel[i-1])
        plt.ylabel(ylabel[i-1])
        if title[i-1]=='Signals':     
            plt.xticks(np.linspace(0,(data['results']['SampleRate']*data['results']['ModellingTime']).item(),6),np.round(np.linspace(0,data['results']['ModellingTime'].item(),6),5))
        if title[i-1]=='Spectrum':
            plt.xlim((0,freq_lim))

    fig.suptitle('Sensor %d, Z %d ,X %d ,Y %d, %s' % (name,int(package.split('_')[0]),int(package.split('_')[1]),int(package.split('_')[2]),package.split('_')[-1]))
    #a=copy.deepcopy(fig)
    result.update({'fig_'+str(name)+'_sensor':fig})

    k+=1
    
label=str(label)+'_result'
ext_label=data['ext_label'].decode('utf-8')

path=job.save_package(label=label,fields=dict(N=N,unique=unique,ext_label=ext_label,altitude=altitude,convert_points=convert_points,answer=answer),files=dict(point=point,sp_data=sp_data,field=field),images=result)


results_file=[s for s in files if 'results' in s][0]
results_path=os.path.abspath(results_file)
move(results_path,str(path)+'/files/'+'results.h5')