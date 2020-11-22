from tmdb import *
from stats import *
from expand import *

dict_operations = {
    0: "Costruzione/Aggiornamento del Database generale;",
    1: "Costruzione/Aggiornamento del Database cast/crew;",
    2: "Statistiche",
    3: "Esci"
}

print("\nCosa vuoi fare?")
for n in dict_operations:
    print(str(n) + " for " + str(dict_operations[n]))
filter = input()
try:
    filter = int(filter)
except:
    print("Errore")

if filter == 0:
    tmdb_py()
    expand()
if filter == 1:
    print("Costruzione CREW")
    crew_count()
    print("Costruzione CAST")
    cast_count()
if filter == 2:
    dict_stats = {
        0: "Film visti per anno di rilascio;",
        1: "Film visti per anno di visione;",
        2: "Persone più presenti nel database;",
        3: "Esci"
    }
    print("\nSTATISTICHE\nCosa vuoi fare?")
    for n2 in dict_stats:
        print(str(n2) + " for " + str(dict_stats[n2]))
    filter2 = int(input())
    if filter2 == 0:
        try:
            watched_by_release_year()
        except:
            print("Errore, verifica di aver eseguito la costruzione del DB")
            pass
    if filter2 == 1:
        try:
            watched_by_year()
        except:
            print("Errore, verifica di aver eseguito la costruzione del DB")
            pass
    if filter2 == 2:
        try:
            filtering_op()
        except:
            print("Errore, verifica di aver eseguito la costruzione di entrambi i DB")
            pass

if filter == 3:
    pass