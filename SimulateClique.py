# -*- coding: utf-8 -*-
from __future__ import division #~ Domysle dzielenie int jako liczb float
from igraph import *     #~ Do symulacji grafu
import random            #~ Do wybierania losowych elementow z listy
import matplotlib.pyplot as plt    #~ Do rysowania wykresow
from  matplotlib import rc
import itertools        #~ do list i iteratorow
import numpy as np        #~ Do np.arange
import time                #~ Do diagnostyki czasu wykonania
import os                #~ Do sprawdzania istnienia folderów
import gzip                #~ Do pakowania plikow wynikowych
import cPickle as pickle
#~ Do zrobienia:
#~ 0. Skrypty do analizy przepisac
#~ 1. Multithreading: http://www.tutorialspoint.com/python/python_multithreading.htm
#~ 2. Przezucic do oddzielnego pakietu/modulu/skryptu funkcje 
#~ 3. Zmienic logike na programu na wykonywanie funkcji a nie imperatywnie - zrobione
#~ 4. Uladnic diagnostyke
#~ 5. Dodac GUI
#~ 6. Przepisac wszystko na C++ ;)
from FilesManagment import CheckFolder, CompressFile, CompressData, FindFileNumber, SaveToFileNumberOfFiles

def wypiszDane(g, KlikList, stg):
    print "ilosci wierzcholkow:", g.vcount()
    print "ilosci polaczen:", g.ecount()
    print "sredniego stopnia:", round(mean(g.degree()), 2)
    print "ilosci klik:", len(KlikList)
    print "wielkosc klik:", stg['CONST_CLIQUE']
    if 'CONST_START_MAGNETIZATION' in stg:
        print "start_mag:", stg['CONST_START_MAGNETIZATION']


def zapisywanie_danych(j, g, M, Mlist, KlikList, stg):

    #~ Dane do dodatkowego pliku opisujacego zapisane dane
    daneWrite = stg.copy()
    daneWrite['WYN_meanG'] = round(mean(g.degree()), 2)
    daneWrite['WYN_j'] = j
    daneWrite['WYN_len(KlikList)'] = len(KlikList)
    daneWrite['WYN_M'] = M

    # daneWrite = '''CONST_VERTICES\n{}\nCONST_EDGES\n{}\nCONST_SIM_COUNT\n{}\nCONST_PRINT\n{}\nCONST_TIME\n{}\nmeanG\n{}\nj\n{}\nlen(KlikList)\n{}\nM\n{}\nwielkosc klik\n{}'''.format(stg['CONST_VERTICES'], stg['CONST_EDGES'], stg['CONST_SIM_COUNT'], stg['CONST_PRINT'], stg['CONST_TIME'], round(mean(g.degree()), 2),j, len(KlikList), M, stg['CONST_CLIQUE'])
    
    #~ Stale folderowo-plikowe
    CONST_STANDARD_PATH = stg['CONST_PATH_BASIC_FOLDER']

    if 'CONST_START_MAGNETIZATION' in stg:
        CONST_STANDARD_RAW_PATH = os.path.join(CONST_STANDARD_PATH, 'RawDataMag', 'klik' + str(stg['CONST_CLIQUE']), 'mag_start', '{:0<5}'.format(stg['CONST_START_MAGNETIZATION']))
        # CONST_STANDARD_WYK_PATH = os.path.join(CONST_STANDARD_PATH, 'Wykresy', 'klik' + str(stg['CONST_CLIQUE']), 'mag_start', '{:0<5}'.format(stg['CONST_START_MAGNETIZATION']))
        CONST_STANDARD_WYK_PATH = os.path.join(CONST_STANDARD_PATH, 'Wykresy', 'klik' + str(stg['CONST_CLIQUE']))#, 'mag_start', '{:0<5}'.format(stg['CONST_START_MAGNETIZATION']))
    else:
        CONST_STANDARD_RAW_PATH = os.path.join(CONST_STANDARD_PATH, 'RawDataMag', 'klik' + str(stg['CONST_CLIQUE']), 'stopnie', str(stg['CONST_MEAN_k']))
        CONST_STANDARD_WYK_PATH = os.path.join(CONST_STANDARD_PATH, 'Wykresy', 'klik' + str(stg['CONST_CLIQUE']), 'stopnie',  str(stg['CONST_MEAN_k']))

    CONST_PATH_FILES_NUMBER = os.path.join(CONST_STANDARD_RAW_PATH, 'filesCount.txt')
    CONST_GENERATED_FILES    = 2
    
    SPECIALdirectoryRAW = os.path.join(CONST_STANDARD_RAW_PATH, 'k' + str(int(round(Mlist[-1],0))))
    CheckFolder(SPECIALdirectoryRAW)
    
    if stg['CONST_OVERRIDEN']:
        fileNumber = i
    elif os.path.isfile(CONST_PATH_FILES_NUMBER):
        with open(CONST_PATH_FILES_NUMBER, 'r+') as f_n:
            fileNumber = eval(f_n.read())
            f_n.seek(0) #~ Bufor na poczatek pliku
            f_n.write(str(fileNumber + 1))
    else:
        fileNumber = int(FindFileNumber(CONST_STANDARD_RAW_PATH) // CONST_GENERATED_FILES)
        with open(CONST_PATH_FILES_NUMBER, 'w') as f_n:
            f_n.write(str(fileNumber + 1))
        
    path_Data = os.path.join(SPECIALdirectoryRAW, 'simResultsData'+ str(fileNumber))
    path_Opis = os.path.join(SPECIALdirectoryRAW, 'simResultsOpis'+ str(fileNumber))
    CompressData(str(Mlist), path_Data, pickling=True)
    CompressData(daneWrite, path_Opis, jsoning = True)
    
    CheckFolder(CONST_STANDARD_WYK_PATH)
    if 'CONST_START_MAGNETIZATION' in stg:
        filepathWYK = os.path.join(CONST_STANDARD_WYK_PATH, 'mag_start{:0<5} file_nb{}.png'.format(stg['CONST_START_MAGNETIZATION'], fileNumber))
    else:
        filepathWYK = os.path.join(CONST_STANDARD_WYK_PATH, 'Magnetyzacja'+ str(fileNumber) +'.png')

    #~ Plotowanie
    plt.plot(Mlist) #~ Tworzenie wykresow magnetyzacji
    plt.ylabel('Magnetyzacja')
    plt.xlabel('Krok (' + str(j) + ' MCS)')
    plt.title(u'Ilość węzłów: {}, połączeń: {}'.format(stg['CONST_VERTICES'], stg['CONST_EDGES']))
    plt.ylim(0,1)
    plt.savefig(filepathWYK, bbox_inches='tight', dpi = 300)
    plt.clf()

def zapisz_magnetyzacje_i_end_check(j, Mlist, g, stg):
    if j % (stg['CONST_VERTICES']//100) == 0:#~ 1000) == 0: 
        #~ Zapisywanie magnetyzacji raz na jakis czas
        M = Magnetyzacja(g, stg)    #~ "Ciezkie" obliczenie czasowo - tyle ile reszta MCS
        Mlist.append(M) #~ Zapisanie magnetyzacji
        if stg['CONST_PRINT']: print 'Magnetyzacja',j,' : ', M
        return j > stg['CONST_VERTICES']*stg['CONST_SIM_LONG']
        #~ dla 3 klik: 300: #~or (not ((M > 0.001) and (M < 0.999))):

def Magnetyzacja(g, stg):
    'Oblicza magnetyzacje grafu g.'
    return sum(g.vs["stan"])/stg['CONST_VERTICES']

def czySaKliki(KlikList):
    return len(KlikList) > 0

def inicjalizacja(stg):
    #~ Tworzenie grafu losowego Erdos_Renyi
    g = Graph.Erdos_Renyi(n=stg['CONST_VERTICES'], m=stg['CONST_EDGES']) 
    #~ Usuniecie izolowanych wierzcholkow      
    g.delete_vertices(g.vs.select(_degree=0))    
    #~ Obsadzanie kazdego wezla losowym spinem
    if 'CONST_START_MAGNETIZATION' in stg:
        g.vs['stan'] = np.array(np.random.random_sample(stg['CONST_VERTICES']) > (1-stg['CONST_START_MAGNETIZATION']), np.int)
    else:
        g.vs['stan'] = [random.randint(0, 1) for x in range(stg['CONST_VERTICES'])] 		
    M = Magnetyzacja(g, stg)	
    #~ Lista w ktorej sa zbierane magnetyzacje dla kolejnych wielokrotnosci krokow	
    Mlist = []		
    Mlist.append(M)
    stg['WYN_REAL_START_MAG'] = M
    #~ licznik po ilosci MCS 
    j = 0
    #~ Lista z klikami   
    KlikList = g.cliques(min = stg['CONST_CLIQUE'], max = stg['CONST_CLIQUE']) 
    return j, g, M, Mlist, KlikList


def MCS_steps(j, g, Mlist,  KlikList, stg):    
    'Glowna petla jednego kroku (MCS)'
    while True: 
        ranTroj = random.choice(KlikList) #~ Wybieramy losowa trojke
        
        stanKliki = 0
        for l in ranTroj: #~ Ustalamy stan kliki
            stanKliki += g.vs[l]['stan']
        
        if stanKliki in (0, stg['CONST_CLIQUE']):
            stanKliki //= stg['CONST_CLIQUE'] #~ stanKliki -> {0,1}
            itClique = itertools.cycle(range(stg['CONST_CLIQUE']))
            itClique.next()
            for d in range(stg['CONST_CLIQUE']): #~ Wykonanie testowego modelu
                for k in set(g.neighbors(ranTroj[d])).intersection(g.neighbors(ranTroj[itClique.next()])):
                    g.vs[k]['stan'] = stanKliki
                    # To chyba dziala tak ze:
                    # robi to stg['CONST_CLIQUE'] razy:
                    # bierze wszystkich sasiadow jednego wezla i potem drugiego wezla i robi przeciecie
                    # i dla calego przeciecia zmienia stan
                    # pytaniem pozostaje po co jest itertool.cycle i next, bo w sumie sie to wykonuje 9 razy a powinno 3? jednak nie; wszystko jest ok?!

			# TODO: zaznaczanie ze dana czesc grafu nie musi byc sprawdzana i zmieniana w jakiejsc zmienne edga, jak to potem odwrocic?

        j += 1 #~ Licznik MCS
        if zapisz_magnetyzacje_i_end_check(j, Mlist, g, stg): break #~ Wyjscie z MCS
    return j

def jedna_symulacja(stg):
    'Petla po powtorzeniach symulacji dla roznych grafow'
    for i in range(stg['CONST_SIM_COUNT']):
        print '\nRozpoczynam symulacje nr:', i, 'dla: '
        j, g, M, Mlist, KlikList = inicjalizacja(stg)     
        wypiszDane(g, KlikList, stg)
        if not czySaKliki(KlikList):
            print 'Brak klik - Koniec'
            break
        j = MCS_steps(j, g, Mlist,  KlikList, stg)
        print 'Magnetyzacja koncowa', j, ' : ', Mlist[-1]    
        zapisywanie_danych(j, g, M, Mlist, KlikList, stg)
        del g
    print 'Koniec jednej symulacji'

# CONST
# START, STOP, STEP = 61.25, 61.75, 0.5
if __name__ == '__main__':
    # podstawowy skrypt do badania wlasnosci
    rc('font', family='Arial') #Plotowanie polskich liter
    #~ Definicje stalych symulacji
    stg = {
        'CONST_CLIQUE'    : 3,      #~ Wielkosc kliki
        'CONST_VERTICES'  : 5000,    #~ Ilosc wezlow
        'CONST_SIM_COUNT' : 1,      #~ Ilosc powtorzen symulacji
        'CONST_PRINT'     : False,  #~ Czy drukowac magnetyzacje co CONST_VERTICES krokow?
        'CONST_TIME'      : True,   #~ Czy przeprowadzac i drukowac wyniki diagnostyki?
        'CONST_FOLDER'    : "",     #~ Nic nie robi
        'CONST_OVERRIDEN' : False,  #~ Czy ma nadpisywac pliki podczas zapisywania wynikow
        'CONST_COMPRESS'  : True,   #~ Czy ma kompresowac dane przez zapisem    
        'CONST_SIM_LONG'  : 14,     # ile wielkosci N ma liczyc
        'CONST_PATH_BASIC_FOLDER' : 'Wyniki_pickle',
    }

    START, STOP, STEP = 24.00, 30.00, 1.0
    for p in np.arange(START,STOP + STEP,STEP):
        stg['CONST_EDGES']  = int(round(p * stg['CONST_VERTICES'] // 2, 0)) #~ Ilosc polaczen
        stg['CONST_MEAN_k'] = round(stg['CONST_EDGES']/stg['CONST_VERTICES']*2, 1)
        jedna_symulacja(stg)

    print 'Koniec Programu'

# http://igraph.org/python/doc/python-igraph.pdf
# has_key is depreciated
