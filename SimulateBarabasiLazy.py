# -*- coding: utf-8 -*-
from __future__ import division #~ Domysle dzielenie int jako liczb float
import ipyparallel as ipp
# from SimulateClique import jedna_symulacja
import numpy as np   

def BA_lazy_faz(p):
    def simulation(x):
        stg = {            
            'CONST_PRINT'     : False,  #~ Czy drukowac magnetyzacje co CONST_VERTICES krokow?
            'CONST_OVERRIDEN' : False,  #~ Czy ma nadpisywac pliki podczas zapisywania wynikow 
            'CONST_VERTICES'  : 10000,    #~ Ilosc wezlow
            'CONST_SIM_COUNT' : 1,      #~ Ilosc powtorzen symulacji
            'CONST_SIM_LONG'  : 10000,     # ile wielkosci N ma liczyc            
            'CONST_PATH_BASIC_FOLDER' : 'now/complex_networks_sim/Wyniki_barabasi_lazy_fazowe',
            'CONST_MODEL'             : 'lazy',  
            'CONST_MODEL_BASIC_VAL'   : 'CONST_START_MAGNETIZATION',
            'CONST_NETWORK_MODEL'     : 'barabasi',
            'CONST_BARABASI_m'        : 4,            
            'CONST_START_MAGNETIZATION' : x
        }

        k = 8
        stg['CONST_EDGES']  = int(round(k * stg['CONST_VERTICES'] // 2, 0)) #~ Ilosc polaczen
        stg['CONST_MEAN_k'] = round(stg['CONST_EDGES']/stg['CONST_VERTICES']*2, 1)    
        
        import sys
        sys.path.append('/dmj/fizmed/pkowalczyk/now/complex_networks_sim')
        import SimulateClique
        result = SimulateClique.jedna_symulacja(stg)       
        print 'end', k
    return simulation

def BA_clique_faz(p):
    def simulation(x):
        stg = {    
            'CONST_CLIQUE'    : 3,  #~ Wielkosc kliki        
            'CONST_PRINT'     : False,  #~ Czy drukowac magnetyzacje co CONST_VERTICES krokow?
            'CONST_OVERRIDEN' : False,  #~ Czy ma nadpisywac pliki podczas zapisywania wynikow 
            'CONST_VERTICES'  : 10000,  #~ Ilosc wezlow
            'CONST_SIM_COUNT' : 1,      #~ Ilosc powtorzen symulacji
            'CONST_SIM_LONG'  : 20,  # ile wielkosci N ma liczyc            
            'CONST_PATH_BASIC_FOLDER' : 'now/complex_networks_sim/Wyniki_barabasi_clique_fazowe',
            'CONST_MODEL'             : 'clique',  
            'CONST_MODEL_BASIC_VAL'   : 'CONST_START_MAGNETIZATION',
            'CONST_NETWORK_MODEL'     : 'barabasi',
            'CONST_BARABASI_m'        : 4,            
            'CONST_START_MAGNETIZATION' : x
        }

        k = 8
        stg['CONST_EDGES']  = int(round(k * stg['CONST_VERTICES'] // 2, 0)) #~ Ilosc polaczen
        stg['CONST_MEAN_k'] = round(stg['CONST_EDGES']/stg['CONST_VERTICES']*2, 1)    
        
        import sys
        sys.path.append('/dmj/fizmed/pkowalczyk/now/complex_networks_sim')
        import SimulateClique
        result = SimulateClique.jedna_symulacja(stg)       
        print 'end', k
    return simulation

def BA_clique_normal(p):
    def simulation(x):
        stg = {    
            'CONST_CLIQUE'    : 3,  #~ Wielkosc kliki        
            'CONST_PRINT'     : False,  #~ Czy drukowac magnetyzacje co CONST_VERTICES krokow?
            'CONST_OVERRIDEN' : False,  #~ Czy ma nadpisywac pliki podczas zapisywania wynikow 
            'CONST_VERTICES'  : 10000,  #~ Ilosc wezlow
            'CONST_SIM_COUNT' : 1,      #~ Ilosc powtorzen symulacji
            'CONST_SIM_LONG'  : 20,  # ile wielkosci N ma liczyc            
            'CONST_PATH_BASIC_FOLDER' : 'now/complex_networks_sim/Wyniki_barabasi_clique_normal',
            'CONST_MODEL'             : 'clique',  
            'CONST_MODEL_BASIC_VAL'   : 'CONST_BARABASI_m',
            'CONST_NETWORK_MODEL'     : 'barabasi',
            'CONST_BARABASI_m'        : x,            
            # 'CONST_START_MAGNETIZATION' : 0.5
        }

        k = x*2
        stg['CONST_EDGES']  = int(round(k * stg['CONST_VERTICES'] // 2, 0)) #~ Ilosc polaczen
        stg['CONST_MEAN_k'] = round(stg['CONST_EDGES']/stg['CONST_VERTICES']*2, 1)    
        
        import sys
        sys.path.append('/dmj/fizmed/pkowalczyk/now/complex_networks_sim')
        import SimulateClique
        result = SimulateClique.jedna_symulacja(stg)       
        print 'end', k
    return simulation

def main():
    clients = ipp.Client()
    dview = clients.load_balanced_view()

    results = dview.map(BA_clique_normal(None), [2,3,4,5,6,7,8,9,10,11][::-1]*1)
    print list(results)    
    # results = dview.map(BA_clique_normal(None), [4,10,20,25,30,33,37,40]*4)
    # print list(results)
    # results = dview.map(BA_lazy_faz(None), [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]*8)
    # print list(results)
    # results = dview.map(BA_clique_faz(None), [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]*8)
    # print list(results)
    print 'Koniec Programu'

if __name__ == '__main__':
    # stg = {
    #     # 'CONST_CLIQUE'        : 3,      #~ Wielkosc kliki
    #     'CONST_VERTICES'        : 10000,    #~ Ilosc wezlow
    #     'CONST_SIM_COUNT'       : 1,      #~ Ilosc powtorzen symulacji
    #     'CONST_PRINT'           : False,  #~ Czy drukowac magnetyzacje co CONST_VERTICES krokow?
    #     'CONST_OVERRIDEN'       : False,  #~ Czy ma nadpisywac pliki podczas zapisywania wynikow  
    #     'CONST_SIM_LONG'        : 10000,     # ile wielkosci N ma liczyc
    #     'CONST_PATH_BASIC_FOLDER' : 'Wyniki_barabasi_lazy_fazowe',
    #     'CONST_MODEL'           : 'lazy', #'clique',
    #     'CONST_LAZY_CUT'        : 0.003,
    #     'CONST_MODEL_BASIC_VAL' : 'CONST_START_MAGNETIZATION',
    #     'CONST_NETWORK_MODEL'   : 'barabasi',
    #     'CONST_BARABASI_m'      : 4
    # }

    # k = 8
    # p = 0.5
    # stg['CONST_START_MAGNETIZATION'] = p
    # stg['CONST_EDGES']  = int(round(k * stg['CONST_VERTICES'] // 2, 0)) #~ Ilosc polaczen
    # stg['CONST_MEAN_k'] = round(stg['CONST_EDGES']/stg['CONST_VERTICES']*2, 1)
    # jedna_symulacja(stg)
    main()
    