import pandas as pd
import matplotlib.pyplot as plt
from time import sleep
import sys
from gettinginfo_tmdb import *
from collections import Counter

dict_crew = {
    0: "Actors",
    1: "Director",
    2: "Producer",
    3: "Writer",
    4: "Editor"
}

'''
    5: "Director of Photography"
    6: "Sound",
    7: "Production Designer",
    8: "Art Direction",
    9: "Set Decoration",
    10: "Visual Effects",
    11: "Original Music Composer",
    12: "Costume Design",
    13: "Makeup Department Head"
'''

#GENERAL STATS
def general(db,diary):
    sum = db['runtime'].sum()
    sum = (sum/60)
    print("\nTotal runtime: "+str(round(sum,3)) +" hours")
    print("Total movies watched (included rewatch): " + str(len(db)))
    types = ['language','country','genre','studios']
    for type in types:
        gen = general_count(db,type)
        print("\nTotal number of "+str(type) +": "+ str(len(gen)))
        print("Top 5 "+str(type))
        for i in range(5):
            number = i+1
            out1 = gen.iloc[i][0]
            out2 = gen.iloc[i][1]
            print(str(number) +" " + str(out1)+ ": " +str(out2))

#WATCHED MOVIES BY RELEASE YEAR
def watched_by_release_year(watched):
    range = watched['Year'].max() - watched['Year'].min()
    plt.hist(watched['Year'], bins=range + 1, rwidth=0.8)
    plt.show()

#NUM OF MOVIES WATCH BY YEAR
def watched_by_year(diary):
    max = int(diary.max())
    min = int(diary.min())
    range = max - min
    plt.hist(diary, bins=range + 1, rwidth=0.8)
    plt.show()

#MOST FREQUENT CREW CSV
def crew_count(db):
    filter_col = [col for col in db if col.startswith('crew')]
    x = 0
    crew = []
    for col in filter_col:
        crew1 = db[col].dropna().tolist()
        crew = crew + crew1
    count = Counter(crew)
    df = pd.DataFrame(count.items(), columns=['crew', 'sum'])
    df = df.sort_values(by=['sum'], ascending=False)
    return df


#MOST FREQUENT CAST CSV
def cast_count(db):
    filter_col = [col for col in db if col.startswith('cast')]
    x = 0
    cast = []
    for col in filter_col:
        cast1 = db[col].dropna().tolist()
        cast = cast + cast1
    count = Counter(cast)
    df = pd.DataFrame(count.items(), columns=['cast', 'sum'])
    df = df.sort_values(by=['sum'], ascending=False)
    return df

def general_count(db,type):
    type = str(type)
    filter_col = [col for col in db if col.startswith(type)]
    cast = []
    for col in filter_col:
        cast1 = db[col].dropna().tolist()
        cast = cast + cast1
    count = Counter(cast)
    df = pd.DataFrame(count.items(), columns=['cast', 'sum'])
    df = df.sort_values(by=['sum'], ascending=False)
    return df

#MOST RATED CAST
def cast_rate(db):
    stringa = 'cast'
    filter_col = [col for col in db if col.startswith(stringa)]
    new_db2 = pd.DataFrame()
    for col in filter_col:
        new_db = db[[col, 'rate']]
        new_db.columns = [stringa, 'rate']
        new_db2 = pd.concat([new_db2, new_db]).dropna()

    db = new_db2.reset_index(drop=True)
    db = (db.groupby(stringa).agg({stringa: 'count', 'rate': 'mean'}))
    db.index.name = None
    db.reset_index(level=0, inplace=True)
    db.columns = [stringa, 'sum', 'avg']
    db = db[db['sum'] > 3].sort_values(by=['avg'], ascending=False)
    return db

def crew_rate(db):
    stringa = 'crew'
    filter_col = [col for col in db if col.startswith(stringa)]
    new_db2 = pd.DataFrame()
    for col in filter_col:
        new_db = db[[col, 'rate']]
        new_db.columns = [stringa, 'rate']
        new_db2 = pd.concat([new_db2, new_db]).dropna()

    db = new_db2.reset_index(drop=True)
    db = (db.groupby(stringa).agg({stringa: 'count', 'rate': 'mean'}))
    db.index.name = None
    db.reset_index(level=0, inplace=True)
    db.columns = [stringa, 'sum', 'avg']
    db = db[db['sum'] > 3].sort_values(by=['avg'], ascending=False)
    return db

#MOVIE MAP
def movie_country(db):
    filter_col = [col for col in db if col.startswith('country')]
    x = 0
    country = []
    for col in filter_col:
        country1 = db[col].dropna().tolist()
        country = country + country1
    count = Counter(country)
    df = pd.DataFrame(count.items(), columns=['country', 'sum'])
    df = df.sort_values(by=['sum'], ascending=False)
    return df
    return country

def movie_map(db):
    import plotly.express as px
    import pycountry
    list_alpha_2 = [i.alpha_2 for i in list(pycountry.countries)]
    list_alpha_3 = [i.alpha_3 for i in list(pycountry.countries)]
    list_alpha = [i.name for i in list(pycountry.countries)]
    list1 = pd.DataFrame({'a2':list_alpha_2,'a3':list_alpha_3,'name':list_alpha})
    #db = pd.read_csv("output/country_count.csv", low_memory=False)
    db['a3'] = ""
    db['name'] = ""
    db = db.set_index('country')
    list1 = list1.set_index('a2')
    db.update(list1)
    db.reset_index(inplace=True)
    import numpy as np
    db['color'] = np.log10(db['sum'])
    fig = px.choropleth(db, locations="a3",
                        color="color",
                        hover_name="name",
                        hover_data=['sum'],
                        )
    fig.update_geos(projection_type="natural earth")
    fig.show()

#FILTRAGGIO
def filtering_op(cast,crew,num2):
    num2 = int(num2)

    for num in dict_crew:
        filter = num

        if int(filter) == 0:
            cast2 = cast['cast'].str.split(":", expand=True)
            cast2.columns = ['id', 'name']
            cast = cast['sum']
            cast = pd.concat([cast2, cast], axis=1)
            print("\nNumber of different " + str(dict_crew[int(filter)]) + ": " + str(len(cast)+1))
            print("TOP 10 " + str(dict_crew[int(filter)]) + ":")
            filtering = cast.head(num2).reset_index()

        if int(filter) == 1:
            filter = dict_crew[int(filter)]
            # crew = pd.read_csv("output/crew_count.csv")
            crew2 = crew['crew'].str.split(":", expand=True)
            crew2.columns = ['id', 'role', 'name']
            crew = crew['sum']
            crew = pd.concat([crew2, crew], axis=1)
            filtering = crew[crew['role'] == filter]
            print("\nNumber of different " + str(filter) + "s: " + str(len(filtering)+1))
            print("TOP 10 " + str(filter) + ":")
            filtering = filtering.head(num2).reset_index()

        else:
            try:
                filter = dict_crew[int(filter)]
                filtering = crew[crew['role'] == filter]
                print("\nNumber of different " + str(filter) + "s: "+ str(len(filtering)+1))
                print("TOP 10 " + str(filter) + ":")
                filtering = filtering.head(num2).reset_index()
            except:
                pass

        n = 0
        for id in filtering['id']:
            id = int(id)
            id = str(id)
            name, pic = person_op(id)
            print(str(n + 1) + "\t" + str(name) + "\t" + str(filtering.at[n, 'sum']))
            n = n + 1

def filtering_op_avg(cast,crew,num2):
    num2 = int(num2)

    for num in dict_crew:
        filter = num
        print("\nTop 10 " + dict_crew[int(filter)] + ":")

        if int(filter) == 0:
            cast2 = cast['cast'].str.split(":", expand=True)
            cast2.columns = ['id', 'name']
            cast = cast.drop(columns='cast')
            cast = pd.concat([cast2, cast], axis=1)
            filtering = cast.head(num2).reset_index()

        if int(filter) == 1:
            filter = dict_crew[int(filter)]
            crew2 = crew['crew'].str.split(":", expand=True)
            crew2.columns = ['id', 'role','name']
            crew = crew.drop(columns='crew')
            crew = pd.concat([crew2, crew], axis=1)
            filtering = crew[crew['role'] == filter]
            filtering = filtering.head(num2).reset_index()

        else:
            try:
                filter = dict_crew[int(filter)]
                filtering = crew[crew['role'] == filter]
                filtering = filtering.head(num2).reset_index()
            except:
                pass

        n = 0
        for id in filtering['id']:
            id = int(id)
            id = str(id)
            name, pic = person_op(id)
            print(str(n + 1) + "\t" + str(name) + "\t" + str(round(filtering.at[n, 'avg'],2))
                  + "★"+ "\t" + str(filtering.at[n, 'sum'])+" movies")
            n = n + 1