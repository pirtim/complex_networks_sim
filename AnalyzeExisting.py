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
from PIL import Image

import AnalyzeLazy_fazowe
import AnalyzeLazyTime

def crop_image(filepath):
    image=Image.open(filepath)
    image.load()
    image_data = np.asarray(image)
    image_data_bw = image_data.min(axis=2)
    non_empty_columns = np.where(image_data_bw.min(axis=0)<255)[0]
    non_empty_rows = np.where(image_data_bw.min(axis=1)<255)[0]
    cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))
    image_data_new = image_data[cropBox[0]:cropBox[1]+1, cropBox[2]:cropBox[3]+1 , :]
    new_image = Image.fromarray(image_data_new)
    new_image.save(filepath)

def loadList(filepath, string_form = True):
    with open(filepath, 'rb') as f:
        content = pickle.load(f)
    return np.array(map(float,content[1:-1].split(','))) if string_form else content

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

def example_lazy():
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
    plt.plot(er_x, er_y, label = u'Sieć ER, $N = 10^4, \\langle k \\rangle = 8$ ')
    plt.plot(ba_x, ba_y, label = u'Sieć BA, $N = 10^4, m = 4$ ')
    plt.ylabel(u'Magnetyzacja $m$')
    plt.xlabel(u'Krok symulacji w ilościach $N$')
    plt.ylim(-1,1)
    plt.legend(loc=4)
    plt.grid(True)
    plt.title(u'Przykładowy przebieg symulacji dla modelu ,,leniwego\'\'')
    plt.rcParams['figure.figsize'] = np.array([5,4])*1.5 
    fig.savefig(filepath_plot, dpi = 140)
    print 'Plotted to: {}'.format(filepath_plot)
    crop_image(filepath_plot)
    print 'Cropped {}'.format(filepath_plot)

def lazy_phase():
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
    plt.plot(er_x, er_y, label = u'Sieć ER, $N = 10^4, \\langle k \\rangle = 8$ ')
    plt.plot(ba_x, ba_y, label = u'Sieć BA, $N = 10^4, m = 4$ ')
    plt.ylabel(u'Magnetyzacja $m$')
    plt.xlabel(u'Krok symulacji w ilościach $N$')
    plt.ylim(-1,1)
    plt.legend(loc=4)
    plt.grid(True)
    plt.title(u'Przykładowy przebieg symulacji dla modelu ,,leniwego\'\'')
    plt.rcParams['figure.figsize'] = np.array([5,4])*1.5 
    fig.savefig(filepath_plot, dpi = 140)
    print 'Plotted to: {}'.format(filepath_plot)
    crop_image(filepath_plot)
    print 'Cropped {}'.format(filepath_plot)


if '__main__' == __name__:
    example_lazy()
