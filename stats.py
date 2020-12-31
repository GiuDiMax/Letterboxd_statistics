import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from prettytable import PrettyTable

dict_crew = {
    0: "Actors",
    1: "Director",
    2: "Producer",
    3: "Writer",
    4: "Editor"
}

people = ['actor', 'director', 'producer', 'writer', 'editor',
          'cinematography', 'production-design', 'art-direction',
          'set-decoration', 'visual-effects', 'composer', 'sound',
          'costumes', 'make-up']

#GENERAL STATS
def general(db):
    sum = db['runtime'].sum()
    sum = (sum/60)
    print("\nTotal runtime: "+str(round(sum,3)) +" hours")
    print("Total movies watched (included rewatch): " + str(len(db)))
    types = ['language','country','genre','studio']
    for type in types:
        gen = general_count(db, type)
        print("\nTotal number of "+str(type) +": "+ str(len(gen)))
        print("Top 5 "+str(type))
        for i in range(5):
            number = i+1
            out1 = gen.iloc[i][0]
            out2 = gen.iloc[i][1]
            try:
                out1 = out1.split(":",1)[1]
            except:
                pass
            print(str(number) + " - " + str(out1) + ": " + str(out2))

def general_year(db, year):
    sum = db['runtime'].sum()
    sum = (sum/60)
    print("\nTotal runtime: "+str(round(sum,3)) +" hours")
    print("Total movies watched in " + str(year) + " (included rewatch): " + str(len(db)))
    db2 = db[db['year'].astype(int) == int(year)]
    leng = (len(db2) + 1 ) / len(db)
    leng = round(leng*10, 1)
    print(str(year)+"'s movies: " + str(len(db2)+1) +", " + str(leng) +"% of total.")
    types = ['language','country','genre','studio']
    for type in types:
        gen = general_count(db, type)
        print("\nTotal number of "+str(type) +": "+ str(len(gen)))
        print("Top 3 "+str(type))
        for i in range(3):
            number = i+1
            out1 = gen.iloc[i][0]
            out2 = gen.iloc[i][1]
            try:
                out1 = out1.split(":",1)[1]
            except:
                pass
            print(str(number) + " - " + str(out1) + ": " + str(out2))

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

# COUNTING
def general_count(db, string):
    filter_col = [col for col in db if col.startswith(string)]
    people = []
    for col in filter_col:
        people1 = db[col].dropna().tolist()
        people = people + people1
    count = Counter(people)
    df = pd.DataFrame(count.items(), columns=[string, 'sum'])
    df = df.sort_values(by=['sum'], ascending=False)
    return df

def people_count(db, num):
    db.drop_duplicates(subset="uri", keep=False, inplace=True)
    for person in people:
        top = general_count(db, person).head(num)
        #top = top.sort_values(by=['sum'], ascending=False)
        top[person] = (top[person].str.split(":", expand=True))[1]
        top = top.reset_index()
        t = PrettyTable(['n', 'Most frequent ' + str(person) + "s", 'Titles'])
        for x in range(num):
            sum = top.at[x, 'sum']
            name = top.at[x, person]
            t.add_row([str(x+1), name, sum])
        print(t)

# MOST RATED
def top_count(db, string):
    filter_col = [col for col in db if col.startswith(string)]
    new_db2 = pd.DataFrame()
    for col in filter_col:
        new_db = db[[col, 'rate']]
        new_db.columns = [string, 'rate']
        new_db2 = pd.concat([new_db2, new_db]).dropna()
    db = new_db2.reset_index(drop=True)
    db = (db.groupby(string).agg({string: 'count', 'rate': 'mean'}))
    db.index.name = None
    db.reset_index(level=0, inplace=True)
    db.columns = [string, 'sum', 'avg']
    db = db[db['sum'] > 3].sort_values(by=['avg'], ascending=False)
    return db

def people_top_count(db, num):
    db.drop_duplicates(subset="uri", keep=False, inplace=True)
    for person in people:
        top = top_count(db, person).head(num)
        top[person] = (top[person].str.split(":", expand=True))[1]
        top = top.reset_index()
        t = PrettyTable(['n', 'Top ' + str(person) + "s",'Avg', 'Titles'])
        for x in range(num):
            sum = top.at[x, 'sum']
            name = top.at[x, person]
            avg = str(round(top.at[x, 'avg'],2)) + " ★"
            t.add_row([str(x+1), name, avg, sum])
        print(t)

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
    df = df.sort_values(by=['sum'], ascending=False).reset_index(drop=True)
    return df

def movie_map(db):
    import plotly.express as px
    import pycountry
    db = movie_country(db)
    list_alpha_3 = [i.alpha_3 for i in list(pycountry.countries)]
    list_alpha = [i.name for i in list(pycountry.countries)]
    list1 = pd.DataFrame({'a3': list_alpha_3, 'name': list_alpha})
    list2 = pd.DataFrame([['USA', 'USA'], ['GBR', 'UK'],
                          ['SUN', 'USSR'], ['VNM', 'Vietnam'],
                          ['TWN', 'Taiwan'], ['KOR ', 'South Korea']], columns=['a3', 'name'])
    list1 = list1.append(list2).reset_index(drop=True)
    db = db.merge(list1, left_on='country', right_on='name', how='left')

    import numpy as np
    db['color'] = np.log10(db['sum'])
    fig = px.choropleth(db, locations="a3",
                        color="color",
                        hover_name="country",
                        hover_data=['sum'],
                        )
    fig.update_geos(projection_type="natural earth")
    fig.show()