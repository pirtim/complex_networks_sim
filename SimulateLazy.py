# DO NOT USE IT.
# USE SimulateClique.py

from igraph import Graph     #~ Do symulacji grafu
import random            #~ Do wybierania losowych elementow z listy
import matplotlib.pyplot as plt    #~ Do rysowania wykresow

#~ Definicje stalych
CONST_VERTICES  = 4000     #~ Ilosc wezlow
CONST_EDGES     = 20000 #~ Ilosc polaczen
CONST_SIM_COUNT = 1000    #~ Ilosc powtorzen symulacji
CONST_PRINT     = False #~ Czy drukowac magnetyzacje co CONST_VERTICES krokow?
CONST_TIME      = False    #~ Czy przeprowadzac i drukowac wyniki diagnostyki?

#~ Funkcja obliczajaca magnetyzacje dla okreslonego grafu g
def Magnetyzacja(g):
    return sum(g.vs["stan"])*(1./CONST_VERTICES)

def singleSim(i):
	print 'Rozpoczynam symulacje nr:', i     
    g = Graph.Erdos_Renyi(n=CONST_VERTICES, m=CONST_EDGES) #~ Tworzenie grafu losowego Erdos_Renyi
    g.delete_vertices(g.vs.select(_degree=0))
	# TODO: zostawianie tylko polaczanego grafu
    g.vs["stan"] = [random.randint(0, 1) for x in range(CONST_VERTICES)] #~ Obsadzanie kazdego wezla losowym spinem
    M = Magnetyzacja(g)
    Mlist = []     #~ Lista w ktorej sa zbierane magnetyzacje dla kolejnych wielokrotnosci krokow
    Mlist.append(M) 
    j = 0        #~ licznik po ilosci MCS
    
    #~ Glowna petla jednego kroku (MCS)
    while True: 
        ranEdge = random.choice(g.es) #~ Wybieramy losowa krawedz
        
        A = ranEdge.source #~ Pierwszy wierzcholek krawedzi
        B = ranEdge.target #~ Drugi wierzcholek krawedzi
        
        if (g.degree(g.vs[A]) > 1) and (g.degree(g.vs[B]) > 1):            
            Ap = B    #~ <- po liczbach a nie obiektach
            Bp = A    
            
            while Ap == B: #~ Losowanie sasiada A'
                Ap = random.choice(g.neighbors(g.vs[A]))

            while Bp == A: #~ Losowanie sasiada B'
                Bp = random.choice(g.neighbors(g.vs[B]))
            # TODO: TU MOZE BYC BLAD BO MOZE WYLOSWAC TO SAMO Ap == Bp

            #~ print A, B, Ap, Bp
            #~ print g.vs[Ap]["stan"], g.vs[A]["stan"], g.vs[B]["stan"], g.vs[Bp]["stan"]
            
            g.vs[Ap]["stan"] = g.vs[B]["stan"] #~ przypisanie nowych wartosci
            g.vs[Bp]["stan"] = g.vs[A]["stan"] #~ zgodnie z modelem sznajdow    
            j = j + 1

			# TODO: zaznaczanie ze dana czesc grafu nie musi byc sprawdzana i zmieniana w jakiejsc zmienne edga, jak to potem odwrocic?
                                        
            if j % CONST_VERTICES == 0: #~ Zapisywanie magnetyzacji raz na jakis czas
                M = Magnetyzacja(g)    #~ "Ciezkie" obliczenie czasowo - tyle ile reszta MCS        
                Mlist.append(M)
                if CONST_PRINT: print "Magnetyzacja",j," : ", M
                if not ((M > 0.005) and (M < 0.995)):
                    break    

    print "Magnetyzacja koncowa", j, " : ", M 
    
    if Mlist[-1] > 0.995: #~ Zapisanie do pliku magnetyzacji
        f = open(r'Wyniki\RawDataMag\k1\simResults'+ str(i) +'.txt', 'w')
        f.write(str(Mlist))
    else:
        f = open(r'Wyniki\RawDataMag\k0\simResults'+ str(i) +'.txt', 'w')
        f.write(str(Mlist))
    f.close()

    plt.plot(Mlist) #~ Tworzenie wykresow magnetyzacji
    plt.ylabel('Magnetyzacja')
    plt.xlabel('Krok (' + str(j) + ' MCS)')
    plt.ylim(0,1)
    #~ plt.show()
    plt.savefig(r'Wyniki\Wykresy\Magnetyzacja'+ str(i) +'.png', bbox_inches='tight', dpi = 300)
    plt.clf()    
    del g

#~ Petla po powtorzeniach symulacji dla roznych grafow
for i in range(1, CONST_SIM_COUNT):
    singleSim(i)    
print 'Koniec'
