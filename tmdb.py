from gettinginfo_tmdb import *
import sys
import os
from web_scraping import *
import pandas as pd
from time import sleep

def tmdb_py():
    from config import tmdb_api
    tmdb.API_KEY = tmdb_api
    film = pd.read_csv("output/letterboxd_joined.csv")
    film.columns = ['Date', 'Name', 'Year', 'uri', 'Rating','watched','rewatch']
    esiste = 0

    try:
        final_old = pd.read_csv("output/tmdb_scrap.csv")
        esiste = 1
        dframe = final_old.id.isin(film.id).astype(str)
        dframe = pd.DataFrame(dframe)
        dframe.columns = ['check']
        final_old = pd.concat([final_old, dframe], axis=1)
        final_old = final_old[final_old.check != 'False']
        final_old = final_old.drop(['check'], axis=1)
    except:
        pass

    final = pd.DataFrame([{'uri': 0, 'imdb_id': 0, 'tmdb_id': 0,
                           'title': 0, 'release': 0, 'runtime': 0,
                           'genre': 0, 'studios':0, 'crew': 0,
                           'cast': 0, 'language': 0, 'country': 0,
                           'type': 0, 'rate': 0,'watched': 0,'rewatch': 0}]).astype(str)

    #final2 = []
    final = final.drop([0])

    try:
        final_old = pd.read_csv("output/tmdb_scrap_middle_backup.csv")
        numrow = len(final_old)
        print("Find backup file, restore " + str(numrow) + " row.")
        esiste = 1
    except:
        pass

    if esiste == 1:
        si_o_no2 = input('\nDo you want to clean up the file excluding the incorrectly identified lines??'
                         '\nType yes (and then enter), otherwise just hit enter:')
        if si_o_no2 == 'yes':
            final_old = final_old[final_old.imdb_id != 'tt0000000']
            final_old = final_old[final_old['imdb_id'].notna()]
            # film3 = final_old[final_old['imdb'].astype(str).str.startswith('tt')]
            # final_old = film3

    if esiste == 1:
        numrow_ori = len(film)
        film = pd.merge(film, final_old, on='uri', how='outer', indicator=True)
        film = film.loc[film['_merge'] == 'left_only']
        numrow = len(film)
        print("\nAlready find " + str(numrow_ori - numrow)
              + " complete row, there are new " + str(numrow) + "\n")

    film = film.iloc[:, 0:7]
    numrow = len(film)
    x = -1
    e = -1
    errori = ""

    for index, row in film.iterrows():
        x = x + 1
        check = 0
        #imdb_id = 0
        uri = row['uri']
        rate = row['Rating']
        watched = row['watched']
        rewatch = row['rewatch']
        title2 = row['Name']
        year2 = row['Year']
        search = tmdb.Search()
        response = search.movie(query=title2, year=year2)
        try:
            s = search.results
            find = []
            for result in s:
                title = result['title']
                id = result['id']
                release = result['release_date']
                year = str(release[0:4])
                if str(title) == str(title2) and str(year) == str(year2):
                    find.append(id)

            if len(find) == 1:
                id = find[0]
                check, final = movie_information_saving(final, x, id, uri, rate, watched, rewatch)

        except:
            check = 0
            pass

        if check != 'ok':
            try:
                imdb_id = imdb_id_scraping(uri)
                tmdb_id, type2 = imdb_to_tmdb_id(imdb_id)
                if str(type2) == 'movie':
                    check, final = movie_information_saving(final, x, tmdb_id, uri, rate, watched, rewatch)
                if str(type2) == 'tv':
                    check, final = serie_information_saving(final, x, tmdb_id, uri, rate, imdb_id,
                                                            type2, watched, rewatch)
                if str(type2) == 'tv_episode':
                    check, final = episode_information_saving_0(final, x, tmdb_id, uri, rate, imdb_id, type2, title2,
                                                                year2, watched, rewatch)
            except:
                pass

        if check != 'ok':
            e = e + 1
            errori = (str(errori) + "\n- " + str(title2))
            type2 = 'not found'
            imdb_id = 'tt0000000'
            check, final = episode_information_saving_0(final, x, tmdb_id, uri, rate, imdb_id,
                                                        type2, title2, year2, watched, rewatch)

        if (x + 1) % 10 == 0:
            if esiste == 1:
                final2 = pd.concat([final_old, final])
            else:
                final2 = final
            final2.to_csv(r'output/tmdb_scrap_middle_backup.csv', index=False, header=True)

        j = (x + 1) / numrow
        sys.stdout.write('\r')
        sys.stdout.write("[%-60s] %d%%" % ('=' * int(60 * j), 100 * j))
        sys.stdout.flush()
        sleep(0.25)

    print("\n")

    if errori != "":
        errori = "\nNot found titles: " + str(errori + ("\n"))
        print(errori)

    if esiste == 1:
        final = pd.concat([final_old, final])
        print("File merged successfully")
    final.to_csv(r'output/tmdb_scrap.csv', index=False, header=True)
    final.to_csv(r'output/tmdb_scrap.csv.bak', index=False, header=True)
    if os.path.exists("output/tmdb_scrap_middle_backup.csv"):
        os.remove("output/tmdb_scrap_middle_backup.csv")
    print("File saved successfully")