# -*- coding: utf-8 -*-
from __future__ import division #~ Domysle dzielenie int jako liczb float
# from igraph import *     #~ Niepotrzebne

import random            #~ Niepotrzebne
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt #~ Do wykresow
from  matplotlib import rc
import time                #~ Niepotrzebne
import os.path            #~ Do sprawdzania istnienia plikow
import numpy as np        #~ Do operacjach na array
import cPickle as pickle
import json
from FilesManagment import CheckFolder

import AnalyzeLazy_fazowe
import AnalyzeLazyTime


def loadList(filepath):
    with open(filepath, 'rb') as f:
        content = pickle.load(f)
    return np.array(map(float,content[1:-1].split(',')))

def loadDic(filepath):
    with open(filepath, 'r') as f:
        dic = json.load(f)
    return dic

def M_na_m(l):
    return 2*l - 1

def get_data_set(stg):
    stg['PATH_DATA_NAME']= 'simResultsData{}.pickle'.format(stg['FILE_NUM'])
    stg['PATH_OPIS_NAME']= 'simResultsOpis{}.json'.format(stg['FILE_NUM'])

    filepath_data = os.path.join(stg['CONST_PATH_BASIC_FOLDER'], stg['PATH_DATA_NAME'])
    filepath_opis = os.path.join(stg['CONST_PATH_BASIC_FOLDER'], stg['PATH_OPIS_NAME'])
    filepath_plot = os.path.join(stg['DIR_PLOT'], stg['PATH_PLOT'])
    print filepath_data
    print filepath_opis

    wynik = loadList(filepath_data)
    dic = loadDic(filepath_opis)

    wynik_y = M_na_m(wynik)
    dt = dic['CONST_VERTICES']//100
    wynik_x = np.arange(0, len(wynik_y),1)*dt / dic['CONST_VERTICES']
    print len(wynik_x), len(wynik_y)
    print wynik_y
    return wynik_x, wynik_y, filepath_plot

stg_er = {
    'CONST_PATH_BASIC_FOLDER' : r'.\..\get_ssh_data\WynikiERtime\RawDataMag\val_start_8.00000',
    'FILE_NUM' : 794,    
    'DIR_PLOT' : 'Wykresy',
    'PATH_PLOT' : 'exampleERlazy_k8.png'
}

stg_ba = {
    'CONST_PATH_BASIC_FOLDER' : r'.\..\get_ssh_data\WynikiBAtime\RawDataMag\val_start_0.50000',
    'FILE_NUM' : 504,    
    'DIR_PLOT' : 'Wykresy',
    'PATH_PLOT' : 'exampleERlazy_k8.png'
}

er_x, er_y, filepath_plot = get_data_set(stg_er)
ba_x, ba_y, filepath_plot = get_data_set(stg_ba)


rc('font', family='Arial') #Plotowanie polskich liter
fig = plt.figure()
plt.plot(er_x, er_y, label = u'Sieć ER, $N = 10^4$')
plt.plot(ba_x, ba_y, label = u'Sieć BA, $N = 10^4$')
plt.ylabel(u'Magnetyzacja $m$')
plt.xlabel(u'Krok symulacji w jednostkach $N$')
plt.ylim(-1,1)
plt.legend(loc=4)
plt.grid(True)
fig.savefig(filepath_plot)
print 'Plotted to: {}'.format(filepath_plot)

