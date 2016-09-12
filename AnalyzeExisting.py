# -*- coding: utf-8 -*-
from __future__ import division #~ Domysle dzielenie int jako liczb float
# from igraph import *     #~ Niepotrzebne

import random            #~ Niepotrzebne
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt #~ Do wykresow

import matplotlib.ticker as ticker  
from  matplotlib import rc
import time                #~ Niepotrzebne
import os.path            #~ Do sprawdzania istnienia plikow
import numpy as np        #~ Do operacjach na array
import cPickle as pickle
import json
import gzip		
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


def loadJustList(filepath, string_form = True):
    with open(filepath, 'rb') as f:
        content = f.read()
    return np.array(map(float,content[1:-1].split(','))) if string_form else content


def loadListGzip(filepath, string_form = True):
    with gzip.open(filepath, 'rb') as f:
        content = f.read()
    return np.array(map(float,content[1:-1].split(','))) if string_form else content


def loadDic(filepath):
    with open(filepath, 'r') as f:
        dic = json.load(f)
    return dic

def M_na_m(l):
    return 2*l - 1

def get_data_set(stg, number = True, just_data =False, phase = False, time = False):
    if number:
        stg['PATH_DATA_NAME']= 'simResultsData{}.pickle'.format(stg['FILE_NUM'])
        stg['PATH_OPIS_NAME']= 'simResultsOpis{}.json'.format(stg['FILE_NUM'])

    filepath_data = os.path.join(stg['CONST_PATH_BASIC_FOLDER'], stg['PATH_DATA_NAME'])        
    filepath_plot = os.path.join(stg['DIR_PLOT'], stg['PATH_PLOT'])
    print filepath_data
    
    if not just_data:        
        filepath_opis = os.path.join(stg['CONST_PATH_BASIC_FOLDER'], stg['PATH_OPIS_NAME'])        
        print filepath_opis

    wynik = loadList(filepath_data, string_form = not phase and not time)

    if not just_data: 
        dic = loadDic(filepath_opis)
        
    if not phase and not time:
        wynik_y = M_na_m(wynik)
        dt = dic['CONST_VERTICES']//100
        wynik_x = np.arange(0, len(wynik_y),1)*dt / dic['CONST_VERTICES']
    elif phase:
        wynik_x, wynik_y = wynik
        wynik_x = list(wynik_x)
        wynik_y = list(wynik_y)
        wynik_y = [y for (x,y) in sorted(zip(wynik_x, wynik_y), key=lambda pair: pair[0])]
        wynik_x = sorted(wynik_x)
    elif time:
        return wynik, filepath_plot

    
    # print len(wynik_x), len(wynik_y)
    print wynik_x, wynik_y
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
    plt.xlabel(u'Krok symulacji w liczbach $N$')
    plt.ylim(-1,1)
    plt.legend(loc=4)
    plt.grid(True)
    plt.title(u'Przykładowy przebieg symulacji dla modelu ,,leniwego\'\'')
    plt.rcParams['figure.figsize'] = np.array([5,4])*1.5 
    fig.savefig(filepath_plot, dpi = 140)
    print 'Plotted to: {}'.format(filepath_plot)
    crop_image(filepath_plot)
    print 'Cropped {}'.format(filepath_plot)

def example_clique():
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
    plt.xlabel(u'Krok symulacji w liczbach $N$')
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
        'CONST_PATH_BASIC_FOLDER' : r'Wyniki_lazy_fazowe\analyze',
        'PATH_DATA_NAME' : 'faz_dla_lazy_er.pickle',
        'DIR_PLOT' : 'Wykresy',
        'PATH_PLOT' : 'lazy_phase.png'
    }

    stg_ba = {
        'CONST_PATH_BASIC_FOLDER' : r'.\..\get_ssh_data\WynikiBAtime\analyze',
        'PATH_DATA_NAME' :  'faz_dla_lazy_bar.pickle',
        'DIR_PLOT' : 'Wykresy',
        'PATH_PLOT' : 'lazy_phase.png'
    }

    er_x, er_y, filepath_plot = get_data_set(stg_er, number = False, just_data = True, phase = True)
    ba_x, ba_y, filepath_plot = get_data_set(stg_ba, number = False, just_data = True, phase = True)

    rc('font', family='Arial') #Plotowanie polskich liter
    fig = plt.figure()    
    plt.plot(er_x, er_y, 'o--', label = u'Sieć ER, $N = 10^3, \\langle k \\rangle = 22$ ')
    plt.plot(ba_x, ba_y, 'o--', label = u'Sieć BA, $N = 10^4, m = 4$ ')    
    plt.plot([0,1], '-', label = u'Zależność $P_+(p_+) = p_+$ ')
    plt.ylabel(u'Prawdopodobieństwo wyjścia $P_+$')
    plt.xlabel(u'Początkowa część węzłów ze spinem +1, $p_+$')
    plt.ylim(0,1)
    plt.xlim(0,1)
    plt.legend(loc=4)
    plt.grid(True)
    plt.title(u'Prawdopodobieństwo wyjścia dla modelu ,,leniwego\'\'')
    plt.rcParams['figure.figsize'] = np.array([5,4])*1.5 
    fig.savefig(filepath_plot, dpi = 140)
    print 'Plotted to: {}'.format(filepath_plot)
    crop_image(filepath_plot)
    print 'Cropped {}'.format(filepath_plot)

def clique_phase():
    stg_er = {
        'CONST_PATH_BASIC_FOLDER' : r'Wyniki_clique_fazowe\analyze',
        'PATH_DATA_NAME' : 'faz_dla_lazy_er.pickle',
        'DIR_PLOT' : 'Wykresy',
        'PATH_PLOT' : 'clique_phase.png'
    }

    stg_ba = {
        'CONST_PATH_BASIC_FOLDER' : r'.\..\get_ssh_data\WynikiBAtime\analyze',
        'PATH_DATA_NAME' :  'faz_dla_lazy_bar.pickle',
        'DIR_PLOT' : 'Wykresy',
        'PATH_PLOT' : 'clique_phase.png'
    }

    # dane z innego pliku tekstowego
    er_x, er_y = ([0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56], [0.0, 0.0, 0.0, 0.0, 0.1875, 0.625, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    filepath_plot = os.path.join('Wykresy', 'clique_phase.png')

    # dane z innego pliku tekstowego
    ba_x, ba_y = ([0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56], [0.0, 0.0, 0.0, 0.0, 0.0, 0.512, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])

    rc('font', family='Arial') #Plotowanie polskich liter
    fig = plt.figure()    
    plt.plot(er_x, er_y, 'o--', label = u'Sieć ER, $N = 6$ x $10^3$,\n $\\langle k \\rangle = 77$')
    plt.plot(ba_x, ba_y, 'o--', label = u'Sieć BA, $N = 10^5$,\n $m = 12$')   
    # plt.plot([0,1], '-', label = u'Zależność $P_+(p_+) = p_+$ ')
    plt.ylabel(u'Prawdopodobieństwo wyjścia $P_+$')
    plt.xlabel(u'Początkowa część węzłów ze spinem +1, $p_+$')
    plt.ylim(0,1)
    plt.xlim(0,1)
    plt.legend(loc=2)
    plt.grid(True)
    plt.title(u'Prawdopodobieństwo wyjścia dla modelu ,,klikowego\'\'')
    plt.rcParams['figure.figsize'] = np.array([5,4])*1.5 
    fig.savefig(filepath_plot, dpi = 140)
    print 'Plotted to: {}'.format(filepath_plot)
    crop_image(filepath_plot)
    print 'Cropped {}'.format(filepath_plot)


def lazy_time():
    def list_from_dir(d):
        result = []
        for key, value in d.iteritems():
            for i in range(value):
                if key <= 10000:
                    result.append(key)
        return result

    stg_er = {
        'CONST_PATH_BASIC_FOLDER' : r'.\..\get_ssh_data\WynikiERtime\analyze',
        'PATH_DATA_NAME' : 'time_dla_er_lazy_fazowe_k8.pickle',
        'DIR_PLOT' : 'Wykresy',
        'PATH_PLOT' : 'lazy_time_1.png'
    }

    stg_ba = {
        'CONST_PATH_BASIC_FOLDER' : r'.\..\get_ssh_data\WynikiBAtime\analyze',
        'PATH_DATA_NAME' :  'time_dla_er_lazy_fazowe_k8.pickle',
        'DIR_PLOT' : 'Wykresy',
        'PATH_PLOT' : 'lazy_time_2.png'
    }    

    er, filepath_plot = get_data_set(stg_er, number = False, time = True, just_data=True)
    ba, filepath_plot = get_data_set(stg_ba,  number = False,time = True, just_data=True)
    # print er
    # print
    # print ba
    er = list_from_dir(er)
    ba = list_from_dir(ba)

    rc('font', family='Arial') #Plotowanie polskich liter
    fig = plt.figure()

    hist_er, bins_er = np.histogram(er, bins=np.linspace(0, 9999, 30), normed = True)
    hist_ba, bins_ba = np.histogram(ba, bins=np.linspace(0, 9999, 30), normed = True)    

    d_er = (bins_er[1]-bins_er[0]) / 2
    # print hist_er, bins_er+d_er
    # print hist_ba, bins_ba+d_er

    # print len(hist_er), len(bins_er+d_er)
    # print len(hist_ba), len(bins_ba+d_er)
    
    
    plt.plot(bins_er[:-1]+d_er, hist_er,'x--', label = 'Histogram dla sieci ER, $N=10^4$, $\\langle k \\rangle = 8$')
    plt.plot(bins_ba[:-1]+d_er, hist_ba,'o--', label = 'Histogram dla sieci BA, $N=10^4$, $m = 4$')
    
    
    # plt.hist(er, bins=np.linspace, normed = True, label = 'er')
    # plt.hist(ba, bins=30, normed = True, label = 'ba')
    # plt.plot(er_x, er_y, 'o--', label = u'Sieć ER, $N = 6$ x $10^3$,\n $\\langle k \\rangle = 77$')
    # plt.plot(ba_x, ba_y, 'o--', label = u'Sieć BA, $N = 10^5$,\n $m = 12$')   
    # plt.plot([0,1], '-', label = u'Zależność $P_+(p_+) = p_+$ ')
    plt.ylabel(u'Prawdopodobieństwo $P_T(t)$')
    plt.xlabel(u'Krok symulacji w liczbach $N$')
    plt.legend(loc=1)
    plt.grid(True)
    plt.xlim(0,9900)
    plt.title(u'Rozkład czasów relaksacji dla modelu ,,leniwego\'\'')
    plt.rcParams['figure.figsize'] = np.array([5,4])*1.5 
    fig.savefig(filepath_plot, dpi = 140)
    print 'Plotted to: {}'.format(filepath_plot)
    crop_image(filepath_plot)
    print 'Cropped {}'.format(filepath_plot)

def fast():
    rc('font', family='Arial') #Plotowanie polskich liter
    fig = plt.figure()
    plt.plot([52,61],[0.1,0.9])
    plt.ylabel(u'Absolutna magnetyzacja końcowa')
    plt.xlabel(u'Średni stopień wierzchołka $\\langle k \\rangle$')
    # plt.legend(loc=2)
    plt.ylim(0,1)
    plt.xlim(50,75)
    # plt.grid(True)
    plt.title(u'Możliwa do osiągniecia magnetyzacja końcowa dla modelu ,,klikowego\'\'')
    plt.rcParams['figure.figsize'] = np.array([5,4])*1.5 
    filepath_plot = os.path.join('Wykresy','klik_koniec_er_4.png')
    fig.savefig(filepath_plot, dpi = 140)
    # fig.savefig(filepath_plot)
    print 'Plotted to: {}'.format(filepath_plot)
    crop_image(filepath_plot)
    print 'Cropped {}'.format(filepath_plot)

def fast2():
    x1 = np.array([3,4,5,6,7,8,9,10,11,12,13])
    y1 = np.array([0.612,0.738, 0.878, 0.9462, 0.9815, 0.9919, 0.997, 0.9994, 0.9999, 1,1])*2-1

    x2 = np.array([4,5,6,7,8,9,10,11])
    y2 = np.array([0.64631, 0.7616, 0.85635, 0.93016, 0.96546, 0.98727, 0.99434, 0.9982])*2-1

    if len(x1) != len (y1) and len(x2) != len (y2):
        raise ValueError('wrd')
    
    

    rc('font', family='Arial') #Plotowanie polskich liter
    fig = plt.figure()
    plt.plot(x1, y1, 'o--',label = u'Sieć BA, o $N = 10^4$')
    plt.plot(x2, y2, 'o--',label = u'Sieć BA, o $N = 10^5$')
    # plt.plot([52,61],[0.1,0.9])
    plt.ylabel(u'Absolutna magnetyzacja końcowa')
    plt.xlabel(u'Współczynnik $m$ sieci BA')
    # plt.legend(loc=2)
    plt.ylim(0,1)
    plt.xlim(2,13)
    plt.grid(True)
    plt.legend(loc = 4)
    plt.title(u'Możliwa do osiągniecia magnetyzacja końcowa dla modelu ,,klikowego\'\'')
    plt.rcParams['figure.figsize'] = np.array([5,4])*1.5 
    filepath_plot = os.path.join('Wykresy','klik_koniec_ba_1.png')
    fig.savefig(filepath_plot, dpi = 140)
    # fig.savefig(filepath_plot)
    print 'Plotted to: {}'.format(filepath_plot)
    crop_image(filepath_plot)
    print 'Cropped {}'.format(filepath_plot)

def plotuj_fast3(PATH_FILE_3, name, to_x = 200, yticks=True, scale = 0.01, gzip_if = True):    
    if gzip_if:
        result = loadListGzip(PATH_FILE_3)
    else:
        result = loadJustList(PATH_FILE_3, string_form = True)
    result = np.array(result)
    result = result*2 - 1
    print result.shape
    # print type(result)
    # print np.array(result)

    rc('font', family='Arial') #Plotowanie polskich liter
    plt.rcParams['figure.figsize'] = np.array([5,4])*1
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(result)
    # plt.plot(result)
    # fig.ylim(-1,1)
    plt.ylim(-1,1)
    filepath_plot = os.path.join('Wykresy', '{}.png'.format(name))

    scale = 0.01

    # ticks = plt.get_xticks()*scale
    # plt.set_xticklabels(ticks)

    if gzip_if:
        ticks = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x*scale))
        ax.xaxis.set_major_formatter(ticks)
    

    if not yticks:
        plt.gca().yaxis.set_major_locator(plt.NullLocator())

    if gzip_if:
        plt.xlim(0,to_x*int(1/scale))
    else:        
        plt.xlim(0,to_x)
    # ax.yaxis.grid() # horizontal lines
    # ax.xaxis.grid() # vertical lines
    # plt.grid()

    fig.savefig(filepath_plot, dpi = 250)
    # fig.savefig(filepath_plot)
    print 'Plotted to: {}'.format(filepath_plot)
    crop_image(filepath_plot)


def fast3():
    PATH_BASIC = r'E:\DropboxPK\Dropbox\Studia\licencjat'
    PATH_S_BASIC_1 = r'Symulacje12.06\Wyniki\RawDataMag\klik3\stopnie\20.0\k0'
    PATH_FILE_1= r'simResultsData2.txt.gz'
    PATH_FILE_1 = os.path.join(PATH_BASIC, PATH_S_BASIC_1, PATH_FILE_1)
    
    PATH_S_BASIC_2 = r'Symulacje12.06\Wyniki\RawDataMag\klik3\stopnie\27.8\k0'
    PATH_FILE_2= r'simResultsData35.txt.gz'
    PATH_FILE_2 = os.path.join(PATH_BASIC, PATH_S_BASIC_2, PATH_FILE_2)

    PATH_S_BASIC_3 = r'Symulacje12.06\Wyniki\RawDataMag\klik3\stopnie\39.5\k1'
    PATH_FILE_3= r'simResultsData11.txt.gz'
    PATH_FILE_3 = os.path.join(PATH_BASIC, PATH_S_BASIC_3, PATH_FILE_3)

    plotuj_fast3(PATH_FILE_1, name = 'klik_typowa_pd')
    plotuj_fast3(PATH_FILE_2,to_x=1200,  name = 'klik_typowa_pp',yticks = True)
    plotuj_fast3(PATH_FILE_3, name = 'klik_typowa_pg', yticks=True)

# E:\DropboxPK\Dropbox\Studia\licencjat\
    PATH_S_BASIC_4 = r'Symulacje2016.07.07\get_ssh_data\Wykresy\Wykresy'
    PATH_FILE_4 = r'pp_ba.data'
    PATH_FILE_4 = os.path.join(PATH_BASIC, PATH_S_BASIC_4, PATH_FILE_4)
    
    PATH_S_BASIC_5 = PATH_S_BASIC_4
    PATH_FILE_5 = r'ps_ba.data'
    PATH_FILE_5 = os.path.join(PATH_BASIC, PATH_S_BASIC_5, PATH_FILE_5)

    PATH_S_BASIC_6 = PATH_S_BASIC_4
    PATH_FILE_6= r'pg_ba.data'
    PATH_FILE_6 = os.path.join(PATH_BASIC, PATH_S_BASIC_6, PATH_FILE_6)

    plotuj_fast3(PATH_FILE_4, name = 'klik_typowa_pd_ba', gzip_if=False)
    plotuj_fast3(PATH_FILE_5, to_x=1200,  name = 'klik_typowa_pp_ba',yticks=True, gzip_if=False)
    plotuj_fast3(PATH_FILE_6, name = 'klik_typowa_pg_ba',yticks=True, gzip_if=False)

if '__main__' == __name__:
    fast3()
