import pandas as pd

def expand():
    film = pd.read_csv("output/tmdb_scrap.csv")
    film.columns = ['uri', 'imdb_id', 'tmdb_id', 'title',
                    'release', 'runtime', 'genre','studios', 'crew',
                    'cast', 'language', 'country', 'type', 'rate']

    list = {'genre', 'director', 'writer', 'actor', 'language', 'country'}

    film = film[film.imdb_id != 'tt0000000']
    film = film[film['imdb_id'].notna()]

    date = pd.read_csv("input/diary.csv")
    date.columns = ['Date', 'Name', 'Year', 'Letterboxd URI',
                    'Rating', 'Rewatch', 'Tags', 'Watched Date']

    '''
    final = pd.merge(film, date, how='right', left_on='uri', right_on='Letterboxd URI',
             indicator=False, validate = 'one_to_many')
    '''

    crew_list = film.crew.str.split(";", expand=True)
    for x in range(len(crew_list.columns)):
        string = 'crew' + str(x + 1)
        crew_list = crew_list.rename(columns={x: string})

    cast_list = film.cast.str.split(";", expand=True)
    for x in range(len(cast_list.columns)):
        string = 'cast' + str(x + 1)
        cast_list = cast_list.rename(columns={x: string})

    genre_list = film.genre.str.split(";", expand=True)
    for x in range(len(genre_list.columns)):
        string = 'genre' + str(x + 1)
        genre_list = genre_list.rename(columns={x: string})

    language_list = film.language.str.split(";", expand=True)
    for x in range(len(language_list.columns)):
        string = 'language' + str(x + 1)
        language_list = language_list.rename(columns={x: string})

    country_list = film.country.str.split(";", expand=True)
    for x in range(len(country_list.columns)):
        string = 'country' + str(x + 1)
        country_list = country_list.rename(columns={x: string})

    final = pd.concat([film, genre_list, language_list, country_list, cast_list, crew_list], axis=1)
    final["uri"] = final["uri"].str.replace("https://boxd.it/", "")
    final = final.drop(columns=['genre', 'cast', 'crew', 'language', 'country'])
    # final = final.loc[final['uri'] != "0"]

    #print("File espanso e salvato col nome di database.csv")
    final.to_csv(r'output/database.csv', index=False, header=True)

expand()