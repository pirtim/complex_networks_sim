from __future__ import division #~ Domysle dzielenie int jako liczb float
# from igraph import *     #~ Niepotrzebne

import random            #~ Niepotrzebne
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

def plotuj(stg, data):
    fig = plt.figure()
    # plt.errorbar(stopnie, srednieKonca, yerr=stdKonca, fmt='--o')
    plt.plot(data[0],data[1], '--o')
    plt.ylim(0,1)
    plt.xlim(0,1)
    plt.ylabel('Prawdopodobienstwo uzyskanie koncowego stanu sieci *w gore*')
    plt.xlabel('Poczatkowa magnetyzacja, N=1000')
    fig.suptitle('Zaleznosc koncowej magnetyzacji od sredniego stopnia wiercholkow sieci')
    #~ plt.fill_between(x, sredniaData-stdData, sredniaData+stdData, color='grey')
    #~ plt.plot(sredniaData, color='black')
    fig.savefig(os.path.join(stg['CONST_STANDARD_PATH_ANALYZE'],'faz_dla_k{}.png'.format(stg['CONST_CLIQUE'])), dpi = 200)
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

def analyze(stg):
    stg['CONST_STANDARD_PATH_ANALYZE'] = os.path.join(stg['CONST_PATH_BASIC_FOLDER'], 'analyze')
    CheckFolder(stg['CONST_STANDARD_PATH_ANALYZE'])
    stg['CONST_SHORT_RAW_PATH'] = os.path.join(stg['CONST_PATH_BASIC_FOLDER'], 'RawDataMag', 'klik' + str(stg['CONST_CLIQUE']), 'mag_start')

    x, y = [], []

    basic_dir = stg['CONST_SHORT_RAW_PATH']
    for path_file in sorted(os.listdir(basic_dir)):
        down = check_folder_k(0, path_file, basic_dir, stg)
        up   = check_folder_k(1, path_file, basic_dir, stg)
        if up + down != 0:
            x.append(float(path_file))
            y.append(up/(up+down))   
# H:\Dropbox\Studia\licencjat\Symulacje2016.07.07\rewritten\Wyniki_fazowe\RawDataMag\klik3\mag_start\0.010\k0\simResultsOpis0

    wynik = (x,y)
    print wynik
    if stg['CONST_DUMP']:
        with open(os.path.join(stg['CONST_STANDARD_PATH_ANALYZE'], 'raw.data') , 'w') as f:
            f.writelines(str(wynik))
    plotuj(stg, wynik)

if __name__ == '__main__':
    # skrypt do analizowania przejscia fazowego
    rc('font', family='Arial') #Plotowanie polskich liter
    #~ Definicje stalych symulacji
    stg = {
        # 'CONST_CLIQUE'    : 3,      #~ Wielkosc kliki
        'CONST_VERTICES'  : 1000,   #~ Ilosc wezlow
        'CONST_OVERRIDEN' : False,  #~ Czy ma nadpisywac pliki podczas zapisywania wynikow   
        'CONST_DUMP'      : True,   # czy ma zrzucac wektory wynikow 
        'CONST_PATH_BASIC_FOLDER' : 'Wyniki_lazy_fazowe',
        'WYN_meanG' : 24
    }

    analyze(stg)
