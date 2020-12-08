import pandas as pd
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
    #crew.to_csv(r'output/crew_count.csv', index=False, header=True)
    return crew



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
    #cast.to_csv(r'output/cast_count.csv', index=False, header=True)
    return cast


#MOVIE MAP
def movie_country():
    db = pd.read_csv("output/database.csv", low_memory=False)
    db = pd.DataFrame(db)
    filter_col = [col for col in db if col.startswith('country')]
    x = 0
    for col1 in filter_col:
        country = pd.pivot_table(db, columns=col1, aggfunc='size', fill_value=0).reset_index(name='sum')
        country.columns = ['country', 'sum']
        if col1 == 'country1':
            country_new = country
        else:
            country_new = pd.concat([country_new, country]).groupby(['country']).sum().reset_index()

        j = (x + 1) / len(filter_col)
        x = x + 1
        sys.stdout.write('\r')
        sys.stdout.write("[%-60s] %d%%" % ('=' * int(60 * j), 100 * j))
        sys.stdout.flush()
        sleep(0.25)

    country = country_new.sort_values(by=['sum'], ascending=False)
    #country.to_csv(r'output/country_count.csv', index=False, header=True)
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
def filtering_op(cast,crew):
    dict_crew = {
        0: "Actors",
        1: "Director",
        2: "Producer",
        3: "Writer",
        4: "Editor",
        5: "Director of Photography",
        6: "Sound",
        7: "Production Designer",
        8: "Art Direction",
        9: "Set Decoration",
        10: "Visual Effects",
        11: "Original Music Composer",
        12: "Costume Design",
        13: "Makeup Department Head"
    }

    #print("\nPer cosa vuoi filtrare?")
    #for n in dict_crew:
    #    print(str(n) + " - " + str(dict_crew[n]))



    for num in dict_crew:
        filter = num
        print("\nTop 10 " + dict_crew[int(filter)] + ":")

        if int(filter) == 0:
            #cast = pd.read_csv("output/cast_count.csv")
            #cast = pd.DataFrame(cast)
            cast.columns = ['id', 'sum']
            filtering = cast.head(10).reset_index()

        if int(filter) == 1:
            filter = dict_crew[int(filter)]
            # crew = pd.read_csv("output/crew_count.csv")
            crew2 = crew['crew'].str.split(":", expand=True)
            crew2.columns = ['id', 'role']
            crew = crew['sum']
            crew = pd.concat([crew2, crew], axis=1)
            filtering = crew[crew['role'] == filter]
            filtering = filtering.head(10).reset_index()

        else:
            try:
                filter = dict_crew[int(filter)]
                filtering = crew[crew['role'] == filter]
                filtering = filtering.head(10).reset_index()
            except:
                pass

        n = 0
        for id in filtering['id']:
            id = int(id)
            id = str(id)
            name, pic = person_op(id)
            print(str(n + 1) + "\t" + str(name) + "\t" + str(filtering.at[n, 'sum']))
            n = n + 1