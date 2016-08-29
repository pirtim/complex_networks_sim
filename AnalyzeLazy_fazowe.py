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

def plotuj(stg, data):
    fig = plt.figure()
    plt.plot(data[0], data[1], '--o')
    if stg['upper']:
        plt.ylim(0.5,1)
        plt.xlim(0.5,1)
    else:
        plt.ylim(0,1)
        plt.xlim(0,1)
    plt.grid()
    plt.plot((0,1),(0,1),'--')
    plt.ylabel('Prawdopodobienstwo uzyskanie koncowego stanu sieci *w gore*')
    plt.xlabel('Poczatkowa magnetyzacja, N={}'.format(stg['CONST_VERTICES']))
    fig.suptitle('Zaleznosc koncowej magnetyzacji od sredniego stopnia wierzcholkow sieci')
    fig.savefig(os.path.join(stg['CONST_STANDARD_PATH_ANALYZE'], stg['CONST_PATH_WYK'].format() + '.png'), dpi = 200)
    fig.clf()

def check_file(dic, stg):
    stan = True
    if 'CONST_VERTICES' in stg:
        stan = stan and stg['CONST_VERTICES'] == dic['CONST_VERTICES']
    if 'CONST_MEAN_k' in stg:
        stan = stan and stg['CONST_MEAN_k'] == dic['CONST_MEAN_k']
    if 'CONST_START_MAGNETIZATION' in stg:
        stan = stan and stg['CONST_START_MAGNETIZATION'] == dic['CONST_START_MAGNETIZATION']
    return stan

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
            if check_file(dic, stg):
            # if dic['CONST_VERTICES'] == stg['CONST_VERTICES'] and dic['CONST_MEAN_k'] == stg['CONST_MEAN_k']:
                if dic['WYN_M'] == 0:
                    down += 1
                elif dic['WYN_M'] == 1:
                    up += 1
    return down, up

def analyze(stg):
    stg['CONST_STANDARD_PATH_ANALYZE'] = os.path.join(stg['CONST_PATH_BASIC_FOLDER'], 'analyze')
    CheckFolder(stg['CONST_STANDARD_PATH_ANALYZE'])
    stg['CONST_SHORT_RAW_PATH'] = os.path.join(stg['CONST_PATH_BASIC_FOLDER'], 'RawDataMag')

    x, y = [], []
    basic_dir = stg['CONST_SHORT_RAW_PATH']
    for path_file in sorted(os.listdir(basic_dir)):
        down, up = check_folder_simple(path_file, basic_dir, stg)
        if up + down != 0:
            x.append(float(path_file[-7:]))
            y.append(up/(up+down))
# H:\Dropbox\Studia\licencjat\Symulacje2016.07.07\complex_networks_sim\Wyniki_lazy_fazowe\RawDataMag\val_start_0.50000

    wynik = (x,y)
    print wynik
    if stg['CONST_DUMP']:
        with open(os.path.join(stg['CONST_STANDARD_PATH_ANALYZE'], stg['CONST_PATH_WYK'] + '.data') , 'w') as f:
            f.writelines(str(wynik))
    plotuj(stg, wynik)

def analyze_fast():
    stg = {
        # 'CONST_CLIQUE'  : 3,    #~ Wielkosc kliki
        'CONST_VERTICES'  : 10000,  #~ Ilosc wezlow
        'CONST_OVERRIDEN' : False,  #~ Czy ma nadpisywac pliki podczas zapisywania wynikow   
        'CONST_DUMP'      : True,   # czy ma zrzucac wektory wynikow 
        'CONST_PATH_BASIC_FOLDER' : 'Wyniki_barabasi_lazy_fazowe',
        # 'CONST_MEAN_k'    : 77,
        'CONST_PATH_WYK'  : 'faz_dla_lazy_bar',
        'upper' : False
        
    }

    stg['CONST_STANDARD_PATH_ANALYZE'] = os.path.join(stg['CONST_PATH_BASIC_FOLDER'], 'analyze')
    CheckFolder(stg['CONST_STANDARD_PATH_ANALYZE'])
    stg['CONST_SHORT_RAW_PATH'] = os.path.join(stg['CONST_PATH_BASIC_FOLDER'], 'RawDataMag')

    wynik = ([0.0,0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0], [0.0,0.014705882352941176, 0.033707865168539325, 0.10144927536231885, 0.21052631578947367, 0.23529411764705882, 0.34615384615384615, 0.36363636363636365, 0.32894736842105265, 0.4852941176470588, 0.5256410256410257, 0.5909090909090909, 0.4935064935064935, 0.7391304347826086, 0.6438356164383562, 0.8059701492537313, 0.8648648648648649, 0.855072463768116, 0.9605263157894737, 0.9710144927536232, 1.0])

    if stg['upper']:
        wynik_np = np.array(wynik)
        wynik_less = wynik_np[1][wynik_np[0] < 0.5]
        wynik_less = np.array([0]+list((1-wynik_less)[::-1]))
        wynik_up = wynik_np[1][wynik_np[0] >= 0.5]
        wynik_up = (wynik_up+wynik_less) / 2  
        wynik_up[0] *= 2
        wynik = (list(wynik_np[0][wynik_np[0] >= 0.5]), list(wynik_up))

    plotuj(stg, wynik)


if __name__ == '__main__':
    # skrypt do analizowania przejscia fazowego
    # rc('font', family='Arial') #Plotowanie polskich liter
    #~ Definicje stalych symulacji
    stg = {
        # 'CONST_CLIQUE'  : 3,    #~ Wielkosc kliki
        'CONST_VERTICES'  : 10000,  #~ Ilosc wezlow
        'CONST_OVERRIDEN' : False,  #~ Czy ma nadpisywac pliki podczas zapisywania wynikow   
        'CONST_DUMP'      : True,   # czy ma zrzucac wektory wynikow 
        'CONST_PATH_BASIC_FOLDER' : 'Wyniki_barabasi_lazy_fazowe',
        # 'CONST_MEAN_k'    : 77,
        'CONST_PATH_WYK'  : 'faz_dla_lazy_bar'
    }

    analyze(stg)

