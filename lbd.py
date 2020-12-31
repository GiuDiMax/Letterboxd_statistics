import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
from time import sleep
import os

def get_data(url, db, index):
    url = str(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # RUNTIME
    total = soup.find('p', class_="text-link text-footer")
    runtime = str(total).split('">', 1)[1]
    runtime = str(runtime).split('mins', 1)[0]
    runtime = runtime.replace(",","")
    try:
        runtime = int(runtime.strip())
    except:
        runtime = ""
    db.at[index, 'runtime'] = runtime

    # IMDB - TMDB
    try:
        imdb = str(total).split('imdb.com/title/', 1)[1]
        imdb = str(imdb).split('/', 1)[0]
    except:
        imdb = ""
    try:
        tmdb = str(total).split('themoviedb.org/movie/', 1)[1]
        tmdb = str(tmdb).split('/', 1)[0]
    except:
        tmdb = ""

    db.at[index, 'imdb'] = imdb
    db.at[index, 'tmdb'] = tmdb

    # GENERE
    try:
        genres = soup.find('div', {"id": "tab-genres"})
        genres = genres.find_all('a', class_="text-slug")
        genre_list = ""
        for genre in genres:
            name = str(genre)
            name = name.split('/">', 1)[1]
            name = name.split('<', 1)[0]
            if genre_list == "":
                genre_list = str(name)
            else:
                genre_list = str(genre_list) + ";" + str(name)
    except:
        genre_list = ""
    db.at[index, 'genre'] = genre_list

    # DETAILS
    details = soup.find('div', {"id": "tab-details"})
    details = details.find_all('div', class_="text-sluglist")
    for detail in details:
        details2 = str(detail).split('</a>')
        details2 = details2[:-1]
        detail_list = ""
        for detail2 in details2:
            code = detail2.split('href="/', 1)[1]
            code = code.split('/">', 1)[0]
            code = code.split("/",1)
            role = code[0]
            code = code[1]
            name = detail2.split('/">', 1)[1]
            if role == 'studio':
                role2 = role
                if detail_list == "" :
                    detail_list = str(code) + ":" + str(name)
                else:
                    detail_list = str(detail_list) + ";" + str(code) + ":" + str(name)
            else:
                role2 = detail2.split('/films/', 1)[1]
                role2 = role2.split('/', 1)[0]
                name = detail2.split('/">', 1)[1]
                if detail_list == "":
                    detail_list = str(name)
                else:
                    detail_list = str(detail_list) + ";" + str(name)
        db.at[index, role2] = detail_list

    # ACTORS
    try:
        actors = soup.find('div', {"id": "tab-cast"})
        actors = actors.find_all('a', class_="text-slug tooltip")
        actor_list = ""
        for actor in actors:
            name = str(actor)
            code = name.split('/actor/', 1)[1]
            code = code.split('/', 1)[0]
            name = name.split('>', 1)[1]
            name = name.split('<', 1)[0]
            if actor_list == "":
                actor_list = str(code) + ":" + str(name)
            else:
                actor_list = str(actor_list) + ";" + str(code) + ":" + str(name)
    except:
        actor_list = ""
    db.at[index, 'actor'] = actor_list

    # CREWS
    crew = soup.find('div', {"id": "tab-crew"})
    try:
        crews = crew.find_all('div', class_="text-sluglist")
    except:
        crews = ""
    role = ""
    for crew in crews:
        crews2 = str(crew).split('</a>')
        crews2 = crews2[:-1]
        crew_list = ""
        try:
            for crew2 in crews2:
                code = crew2.split('href="/', 1)[1]
                code = code.split('/">', 1)[0]
                code = code.split("/", 1)
                role = code[0]
                code = code[1]
                name = crew2.split('/">', 1)[1]
                if crew_list == "":
                    crew_list = str(code) + ":" + str(name)
                else:
                    crew_list = str(crew_list) + ";" + str(code) + ":" + str(name)
            db.at[index, role] = crew_list
        except:
            pass
    return db

def letterboxd ():
    film = pd.read_csv("output/letterboxd_joined.csv")
    film.columns = ['Date', 'Title', 'Year', 'uri', 'Rate', 'watched', 'rewatch']
    esiste = 0

    db = pd.DataFrame([{'uri': 0, 'imdb': 0, 'tmdb': 0, 'title': 0, 'type': 0,
                        'year': 0, 'runtime': 0, 'rate': 0, 'watched': 0, 'rewatch': 0,
                        'studio': 0, 'country': 0, 'language': 0, 'genre': 0,
                        'actor': 0, 'director': 0, 'producer': 0, 'writer': 0,
                        'editor': 0, 'cinematography': 0, 'production-design': 0,
                        'art-direction': 0, 'set-decoration': 0, 'visual-effects': 0,
                        'composer': 0, 'sound': 0, 'costumes': 0, 'make-up': 0,
                        'co-director': 0}]).astype(str)

    db = db.drop([0])

    try:
        final_old = pd.read_csv("output/lbd_scrap.csv")
        esiste = 1
    except:
        pass

    try:
        final_old = pd.read_csv("output/lbd_scrap_middle_backup.csv")
        numrow = len(final_old)
        print("Find backup file, restore " + str(numrow) + " row.")
        esiste = 1
    except:
        pass

    if esiste == 1:
        numrow_ori = len(film)
        film = pd.merge(film, final_old, on=['uri', 'watched', 'rewatch'], how='outer', indicator=True)
        film['rate'] = film['Rate']
        final_old = film.loc[film['_merge'] == 'both']
        final_old = final_old.drop(columns=['Date','Title','Year','Rate','_merge'])
        film = film.loc[film['_merge'] == 'left_only']
        film = film[['Date','Title','Year','uri','Rate','watched','rewatch']]
        numrow = len(film)
        print("Already find " + str(numrow_ori - numrow)
              + " complete row, there are new " + str(numrow) + "\n")

    x = - 1
    film = film.iloc[:, 0:7]
    film.columns = ['Date', 'Name', 'Year', 'uri', 'Rating', 'watched', 'rewatch']
    numrow = len(film)
    for index, row in film.iterrows():
        x = x + 1
        uri = row['uri']
        db.at[x, 'uri'] = row['uri']
        db.at[x, 'rate'] = row['Rating']
        db.at[x, 'watched'] = row['watched']
        db.at[x, 'rewatch'] = row['rewatch']
        db.at[x, 'title'] = row['Name']
        db.at[x, 'year'] = row['Year']
        db = get_data(uri, db, x)
        j = (x + 1) / numrow
        sys.stdout.write('\r')
        sys.stdout.write("[%-60s] %d%%" % ('=' * int(60 * j), 100 * j))
        sys.stdout.flush()
        sleep(0.25)

        if (x + 1) % 10 == 0:
            if esiste == 1:
                final2 = pd.concat([final_old, db])
            else:
                final2 = db
            final2.to_csv(r'output/lbd_scrap_middle_backup.csv', index=False, header=True)

    if esiste == 1:
        db = pd.concat([final_old, db])
    db.to_csv(r'output/lbd_scrap.csv', index=False, header=True)
    db.to_csv(r'output/lbd_scrap.csv.bak', index=False, header=True)

    if os.path.exists("output/lbd_scrap_middle_backup.csv"):
        os.remove("output/lbd_scrap_middle_backup.csv")
    print("\nFile saved successfully")

'''
db = pd.DataFrame()
index = 0
url = 'https://letterboxd.com/film/lady-bird/genres/'
get_data(url, db, index)
'''