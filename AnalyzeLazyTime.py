from __future__ import division #~ Domysle dzielenie int jako liczb float
# from igraph import *     #~ Niepotrzebne

import random            #~ Niepotrzebne
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt #~ Do wykresow
from  matplotlib import rc
import time                #~ Niepotrzebne
import os.path            #~ Do sprawdzania istnienia plikow
import numpy as np        #~ Do operacjach na array
import cPickle as pickle
import json
from FilesManagment import CheckFolder
        
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
        plt.hist(np.log(np.array(data)), bins=40, normed = True)         
        plt.grid(True)
    else:
        raise ValueError

    plt.ylabel('Ilosc przypadkow')
    plt.xlabel('Czasy')
    fig.suptitle('Histogram czasu trwania symulacji - {}.'.format(type_plot))

    fig.savefig(os.path.join(stg['CONST_STANDARD_PATH_ANALYZE'], stg['CONST_PATH_WYK']+'_{}'.format(type_plot) + '.png'), dpi = 200)
    fig.clf()

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

def check_folder_time(wyn_xy, wyn_x, path_file, basic_dir, stg):
    path = os.path.join(basic_dir, path_file)
    if os.path.exists(path):
        for path_opis in filter(lambda name: name.endswith('.json'), os.listdir(path)):
            with open(os.path.join(path, path_opis), 'r') as f:
                dic = json.load(f)  
            if dic['CONST_SIM_LONG']*dic['CONST_VERTICES'] != dic['WYN_j']+1:
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
    for path_file in sorted(os.listdir(basic_dir)):
        check_folder_time(wyn_xy, wyn_x, path_file, basic_dir, stg)
        # if up + down != 0:
        #     x.append(float(path_file[-7:]))
        #     y.append(up/(up+down))
# H:\Dropbox\Studia\licencjat\Symulacje2016.07.07\complex_networks_sim\Wyniki_lazy_fazowe\RawDataMag\val_start_0.50000

    # wynik = (x,y)
    if stg['CONST_DUMP']:
        with open(os.path.join(stg['CONST_STANDARD_PATH_ANALYZE'], stg['CONST_PATH_WYK'] + '.data') , 'w') as f:
            f.writelines(str(wyn_xy))
    plotuj(stg, wyn_xy, 'dirr')
    plotuj(stg, wyn_x,  'hist')
    plotuj(stg, wyn_x,  'hist_log')
    plotuj(stg, wyn_x,  'log_norm')
    print len(wyn_x)
    print sorted(wyn_xy.iteritems(), key=lambda (x, y): x)

if __name__ == '__main__':
    # skrypt do analizowania przejscia fazowego
    # rc('font', family='Arial') #Plotowanie polskich liter
    #~ Definicje stalych symulacji
    stg = {
        # 'CONST_CLIQUE'    : 3,      #~ Wielkosc kliki
        # 'CONST_VERTICES'  : 1000,   #~ Ilosc wezlow
        'CONST_OVERRIDEN' : False,  #~ Czy ma nadpisywac pliki podczas zapisywania wynikow   
        'CONST_DUMP'      : True,   # czy ma zrzucac wektory wynikow 
        'CONST_PATH_BASIC_FOLDER' : 'Wyniki_lazy_meanK',
        'CONST_MEAN_k'    : 22,
        'CONST_PATH_WYK'  : 'time_dla_lazy'
    }

    analyze(stg)
