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
from FilesManagment import CheckFolder, CompressData   
from PIL import Image

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

#~ Funkcja bierze liste i odwraca tam gdzie sa mniejsze niz 0.5        
def OdwrocMniejsze(lista):
    retlista = np.array(lista)
    if retlista[-1] < 0.5:
        retlista = 1 - retlista
        # [1-x for x in lista]
    return list(retlista)

#~ Funkcja bierze liste i przedloza ja zerami lub jedynkami do zadanej wielkosci
def PrzedlozDo(lista, doIle):
    lenLista = len(lista)
    if lista[-1] > 0.995:
        return np.pad(lista, (0,doIle - lenLista),'constant', constant_values=(1))
    else:
        return np.pad(lista, (0,doIle - lenLista),'constant', constant_values=(0))    

def plotuj(stg, data, type_plot):
    fig = plt.figure()
    if type_plot == 'hist':
        plt.hist(data, bins=80, normed = True)         
        plt.grid(True)
        # plt.hist(data, bins = 20, normed = True, log = True, histtype = 'step')
    elif type_plot == 'hist_log':
        plt.hist(data, bins=np.logspace(1, 4, 40), normed = True)
        plt.gca().set_xscale("log")
        plt.gca().set_yscale("log")            
        plt.grid(True)
        # plt.hist(data, bins = 20, normed = True, log = True, histtype = 'step')
    elif type_plot == 'dirr':
        plt.plot(data.keys(), data.values(), 'o')
    elif type_plot == 'log_norm':    
        print np.log(np.array(data))
        plt.hist(np.log(np.array(data)), bins=40, normed = True)         
        plt.grid(True)
    else:
        raise ValueError

    plt.ylabel(u'Prawdopodobieństwo $P_T(t)$')
    plt.xlabel(u'Zlogarytmowany krok symulacji w liczbach $N$')
    # fig.suptitle('Histogram czasu trwania symulacji - {}.'.format(type_plot))
    plt.title(u'Rozkład zlogarytowanych czasów relaksacji dla modelu ,,leniwego\'\'')

    fig.savefig(os.path.join(stg['CONST_STANDARD_PATH_ANALYZE'], stg['CONST_PATH_WYK']+'_{}'.format(type_plot) + '.png'), dpi = 200)
    print 'Plotted to: {}'.format(os.path.join(stg['CONST_STANDARD_PATH_ANALYZE'], stg['CONST_PATH_WYK']+'_{}'.format(type_plot) + '.png'))
    fig.clf()
    crop_image(os.path.join(stg['CONST_STANDARD_PATH_ANALYZE'], stg['CONST_PATH_WYK']+'_{}'.format(type_plot) + '.png'))

def check_folder_k(spin, path_file, basic_dir, stg):
    path_k = os.path.join(basic_dir, path_file, 'k{}'.format(spin))
    result = 0
    if os.path.exists(path_k):
        for path_opis in filter(lambda name: name.endswith('.json'), os.listdir(path_k)):
            with open(os.path.join(path_k, path_opis), 'r') as f:
                dic = json.load(f)
            if dic['CONST_VERTICES'] == stg['CONST_VERTICES'] and dic['WYN_meanG'] == stg['WYN_meanG']:
                result += 1
    return result

def check_folder_simple(path_file, basic_dir, stg):
    path = os.path.join(basic_dir, path_file)
    up, down = 0, 0
    if os.path.exists(path):
        for path_opis in filter(lambda name: name.endswith('.json'), os.listdir(path)):
            with open(os.path.join(path, path_opis), 'r') as f:
                dic = json.load(f)
            if dic['CONST_VERTICES'] == stg['CONST_VERTICES'] and dic['CONST_MEAN_k'] == stg['CONST_MEAN_k']:
                if dic['WYN_M'] == 0:
                    down += 1
                elif dic['WYN_M'] == 1:
                    up += 1
    return down, up

def check_file(dic, stg):
    stan = True

    if 'CONST_VERTICES' in stg:
        if 'CONST_VERTICES' not in dic:
            return False
        stan = stan and stg['CONST_VERTICES'] == dic['CONST_VERTICES']
    if 'CONST_MEAN_k' in stg:
        if 'CONST_MEAN_k' not in dic:
            return False
        stan = stan and stg['CONST_MEAN_k'] == dic['CONST_MEAN_k']
    if 'CONST_START_MAGNETIZATION' in stg:
        if 'CONST_START_MAGNETIZATION' not in dic:
            return False
        stan = stan and stg['CONST_START_MAGNETIZATION'] == dic['CONST_START_MAGNETIZATION']
    # if not stan and dic['CONST_VERTICES'] == 10000:
    #     print dic
    return stan

def check_folder_time(wyn_xy, wyn_x, path_file, basic_dir, stg):
    path = os.path.join(basic_dir, path_file)
    if os.path.exists(path):
        for path_opis in filter(lambda name: name.endswith('.json'), os.listdir(path)):
            with open(os.path.join(path, path_opis), 'r') as f:
                dic = json.load(f)  
            if dic['CONST_SIM_LONG']*dic['CONST_VERTICES'] != dic['WYN_j']+1 and check_file(dic, stg):
                time = int(dic['WYN_j']/dic['CONST_VERTICES'])
                wyn_x.append(time)
                if time in wyn_xy:
                    wyn_xy[time] += 1
                else:
                    wyn_xy[time] = 1

def analyze(stg):
    stg['CONST_STANDARD_PATH_ANALYZE'] = os.path.join(stg['CONST_PATH_BASIC_FOLDER'], 'analyze')
    CheckFolder(stg['CONST_STANDARD_PATH_ANALYZE'])
    stg['CONST_SHORT_RAW_PATH'] = os.path.join(stg['CONST_PATH_BASIC_FOLDER'], 'RawDataMag')

    wyn_xy = {}
    wyn_x = []
    # x, y = [], []
    basic_dir = stg['CONST_SHORT_RAW_PATH']
    if 'CONST_FAZOWE' in stg and stg['CONST_FAZOWE']:
        for path_file in sorted(os.listdir(basic_dir)):
            basic_dir_inner = os.path.join(basic_dir, path_file)
            for path_file_inner in sorted(os.listdir(basic_dir_inner)):
                check_folder_time(wyn_xy, wyn_x, path_file_inner, basic_dir_inner, stg)

    for path_file in sorted(os.listdir(basic_dir)):
        check_folder_time(wyn_xy, wyn_x, path_file, basic_dir, stg)
# H:\Dropbox\Studia\licencjat\Symulacje2016.07.07\complex_networks_sim\Wyniki_lazy_fazowe\RawDataMag\val_start_0.50000

    if stg['CONST_DUMP']:
        CompressData(wyn_xy, os.path.join(stg['CONST_STANDARD_PATH_ANALYZE'], stg['CONST_PATH_WYK']), pickling=True)

        with open(os.path.join(stg['CONST_STANDARD_PATH_ANALYZE'], stg['CONST_PATH_WYK'] + '.data') , 'w') as f:
            f.writelines(str(wyn_xy))    
    print len(wyn_x)
    print sorted(wyn_xy.iteritems(), key=lambda (x, y): x)
    plotuj(stg, wyn_xy, 'dirr')
    plotuj(stg, wyn_x,  'hist')
    plotuj(stg, wyn_x,  'hist_log')
    plotuj(stg, wyn_x,  'log_norm')

if __name__ == '__main__':
    # skrypt do analizowania przejscia fazowego
    rc('font', family='Arial') #Plotowanie polskich liter
    #~ Definicje stalych symulacji
    stg = {
        # 'CONST_CLIQUE'  : 3,      #~ Wielkosc kliki
        'CONST_VERTICES'  : 1000,   #~ Ilosc wezlow
        'CONST_OVERRIDEN' : False,  #~ Czy ma nadpisywac pliki podczas zapisywania wynikow   
        'CONST_DUMP'      : True,   # czy ma zrzucac wektory wynikow 
        # 'CONST_PATH_BASIC_FOLDER' : 'Wyniki_barabasi_lazy_fazowe',
        'CONST_PATH_BASIC_FOLDER' : 'Wyniki_lazy_meanK',
        'CONST_MEAN_k'    : 22.0,
        'CONST_PATH_WYK'  : 'time_dla_er_lazy_fazowe_k8',
        'CONST_FAZOWE'    : False,         
        'CONST_START_MAGNETIZATION' : 0.5
    }

    analyze(stg)
