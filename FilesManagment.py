# -*- coding: utf-8 -*-
from __future__ import division #~ Domysle dzielenie int jako liczb float
import os
import gzip
import cPickle as pickle
import json

def CheckFolder(directory):
    'Sprawdza czy istnieje folder, jezeli nie - tworzy go.'
    if not os.path.exists(directory):
        os.makedirs(directory)
        
def CompressFile(path):
    'Archiwizuje pliki.'
    with open(path, 'rb') as f_in:
        with gzip.open(path + '.gz', 'wb') as f_out:
            f_out.writelines(f_in)  
    os.remove(path)

def CompressData(content, path, pickling=False, jsoning = False):
    'Zapisuje dane do pliku zaarchiwozowanego. Moze picklowac.'
    if pickling:
        with open(path + '.pickle', 'wb') as f:
            pickle.dump(content, f, -1)
    elif jsoning:
        with open(path + '.json', 'w') as f:        
            json.dump(content, f, sort_keys=True, indent=4)
    else:
        with open(path, 'w') as f:
            f.write(content)

def FindFileNumber(path):
    'Rekursywnie sprawdza ilosc plikow w folderze.'
    return sum([len(files) for r, d, files in os.walk(path)])

def SaveToFileNumberOfFiles(path, number_of_generated_files, num_file = "filesCount.txt"):
    'Rekursywnie sprawdza ilosc plikow w folderze oraz zapisuje do pliku - niesprawdzone'
    fileNumber = int(FindFileNumber(path) // number_of_generated_files) 
    #bylo: CONST_GENERATED_FILES
    # f_n = open(num_file, 'w')
    with open(num_file, 'w') as f_n:
        f_n.write(str(fileNumber))  
    # f_n.close()  