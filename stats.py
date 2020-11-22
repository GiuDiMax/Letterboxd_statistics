import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import sys
from gettinginfo_tmdb import *

#WATCHED MOVIES BY RELEASE YEAR
def watched_by_release_year():
    watched = pd.read_csv("input/watched.csv")
    watched = pd.DataFrame(watched)
    range = watched['Year'].max() - watched['Year'].min()
    plt.hist(watched['Year'], bins=range + 1, rwidth=0.8)
    plt.show()

#NUM OF MOVIES WATCH BY YEAR
def watched_by_year():
    diary = pd.read_csv("input/diary.csv")
    diary = pd.DataFrame(diary)
    diary = diary['Watched Date'].str.split("-", expand=True)
    diary = (diary.iloc[:, 0])
    max = int(diary.max())
    min = int(diary.min())
    range = max - min
    plt.hist(diary, bins=range + 1, rwidth=0.8)
    plt.show()


#MOST FREQUENT CREW CSV
def crew_count():
    db = pd.read_csv("output/database.csv", low_memory=False)
    db = pd.DataFrame(db)
    filter_col = [col for col in db if col.startswith('crew')]
    x = 0
    for col1 in filter_col:
        crew = pd.pivot_table(db, columns=col1, aggfunc='size', fill_value=0).reset_index(name='sum').dropna()
        crew.columns = ['crew', 'sum']
        if col1 == 'crew1':
            crew_new = crew
        else:
            crew_new = pd.concat([crew_new, crew]).groupby(['crew']).sum().reset_index()

        j = (x + 1) / len(filter_col)
        x = x + 1
        sys.stdout.write('\r')
        sys.stdout.write("[%-60s] %d%%" % ('=' * int(60 * j), 100 * j))
        sys.stdout.flush()
        sleep(0.25)

    crew = crew_new.sort_values(by=['sum'], ascending=False)
    crew.to_csv(r'output/crew_count.csv', index=False, header=True)


#MOST FREQUENT CAST CSV
def cast_count():
    db = pd.read_csv("output/database.csv", low_memory=False)
    db = pd.DataFrame(db)
    filter_col = [col for col in db if col.startswith('cast')]
    x = 0
    for col1 in filter_col:
        cast = pd.pivot_table(db, columns=col1, aggfunc='size', fill_value=0).reset_index(name='sum').dropna()
        cast.columns = ['cast', 'sum']
        if col1 == 'cast1':
            cast_new = cast
        else:
            cast_new = pd.concat([cast_new, cast]).groupby(['cast']).sum().reset_index()

        j = (x + 1) / len(filter_col)
        x = x + 1
        sys.stdout.write('\r')
        sys.stdout.write("[%-60s] %d%%" % ('=' * int(60 * j), 100 * j))
        sys.stdout.flush()
        sleep(0.25)

    cast = cast_new.sort_values(by=['sum'], ascending=False)
    cast.to_csv(r'output/cast_count.csv', index=False, header=True)


# FILTRAGGIO
def filtering_op():
    dict_crew = {
        0: "Actors",
        1: "Directing",
        2: "Costume & Make-Up",
        3: "Production",
        4: "Camera",
        5: "Sound",
        6: "Art",
        7: "Visual Effects",
        8: "Editing",
        9: "Lighting",
        10: "Writing",
        11: "Crew"
    }

    print("\nPer cosa vuoi filtrare?")

    for n in dict_crew:
        print(str(n) + " for " + str(dict_crew[n]))
    filter = input()
    if int(filter) == 0:
        pass

    else:
        filter = dict_crew[int(filter)]
        crew = pd.read_csv("output/crew_count.csv")
        crew2 = crew['crew'].str.split(":", expand=True)
        crew2.columns = ['id', 'role']
        crew = crew['sum']
        crew = pd.concat([crew2, crew], axis=1)
        filtering = crew[crew['role'] == filter]
        filtering = filtering.head(10).reset_index()

    n = 0
    for id in filtering['id']:
        name, pic = person_op(id)
        print(str(n + 1) + "\t" + str(name) + "\t" + str(filtering.at[n, 'sum']))
        n = n + 1