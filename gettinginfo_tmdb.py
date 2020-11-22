import tmdbsimple as tmdb
from config import tmdb_api
tmdb.API_KEY = tmdb_api

def serie_information_saving(final,x,tmdb_id,uri,rate,imdb_id, type):
    try:
        serie = tmdb.TV(tmdb_id)
        response = serie.info()

        #imdb_id = response['imdb_id']
        tmdb_id = response['id']
        title = response['name']
        release = response['first_air_date']
        # runtime = response['runtime']
        genre = response['genres']
        language = response['spoken_languages']
        country = response['production_countries']
        type = response['type']

        final.at[x, 'uri'] = uri
        final.at[x, 'imdb_id'] = imdb_id
        final.at[x, 'tmdb_id'] = tmdb_id
        final.at[x, 'title'] = title
        final.at[x, 'release'] = release
        #final.at[x, 'runtime'] = runtime
        final.at[x, 'type'] = type
        final.at[x, 'rate'] = rate

        lang_string = ""
        for lang in language:
            lang = lang['english_name']
            lang_string = str(lang_string) + str(lang) + ";"
        lang_string = lang_string[:-1]
        final.at[x, 'language'] = lang_string

        genre_string = ""
        for gen in genre:
            gen = gen['name']
            genre_string = str(genre_string) + str(gen) + ";"
        genre_string = genre_string[:-1]
        final.at[x, 'genre'] = genre_string

        country_string = ""
        for cou in country:
            cou = cou['name']
            country_string = str(country_string) + str(cou) + ";"
        country_string = country_string[:-1]
        final.at[x, 'country'] = country_string

        people = serie.credits()
        final = crew_cast(final, people, x)

        check = 'ok'

    except:
        check = 0
        pass

    return[check,final]

def episode_information_saving(final,x,tmdb_id,uri,rate,imdb_id,type):
    try:
        episode = tmdb.TV_Episodes(tmdb_id)
        response = episode.info()

        #imdb_id = response['imdb_id']
        tmdb_id = response['id']
        title = response['name']
        release = response['air_date']
        # runtime = response['runtime']
        #genre = response['genres']
        #language = response['languages']
        #country = response['origin_country']
        #type = response['type']

        final.at[x, 'uri'] = uri
        final.at[x, 'imdb_id'] = imdb_id
        final.at[x, 'tmdb_id'] = tmdb_id
        final.at[x, 'title'] = title
        final.at[x, 'release'] = release
        #final.at[x, 'runtime'] = runtime
        #final.at[x, 'genre'] = genre
        final.at[x, 'type'] = type
        final.at[x, 'rate'] = rate

        '''
        lang_string = ""
        for lang in language:
            lang = lang['name']
            lang_string = str(lang_string) + str(lang) + ";"
        lang_string = lang_string[:-1]
        final.at[x, 'language'] = lang_string

        genre_string = ""
        for gen in genre:
            gen = gen['name']
            genre_string = str(genre_string) + str(gen) + ";"
        genre_string = genre_string[:-1]
        final.at[x, 'genre'] = genre_string
        
        country_string = ""
        for cou in country:
            cou = cou['name']
            country_string = str(country_string) + str(cou) + ";"
        country_string = country_string[:-1]
        final.at[x, 'coutry'] = country_string
        '''

        people = episode.credits()
        final = crew_cast(final, people, x)

        check = 'ok'

    except:
        check = 0
        pass

    return[check,final]

def movie_information_saving(final,x,id,uri,rate):
    check = 0
    movie = tmdb.Movies(id)
    response = movie.info()

    imdb_id = response['imdb_id']
    tmdb_id = response['id']
    title = response['title']
    release = response['release_date']
    runtime = response['runtime']
    genre = response['genres']
    language = response['spoken_languages']
    country = response['production_countries']
    type = 'movie'

    final.at[x, 'uri'] = uri
    final.at[x, 'imdb_id'] = imdb_id
    final.at[x, 'tmdb_id'] = tmdb_id
    final.at[x, 'title'] = title
    final.at[x, 'release'] = release
    final.at[x, 'runtime'] = runtime
    final.at[x, 'genre'] = genre
    final.at[x, 'type'] = type
    final.at[x, 'rate'] = rate

    lang_string = ""
    for lang in language:
        lang = lang['english_name']
        lang_string = str(lang_string) + str(lang) + ";"
    lang_string = lang_string[:-1]
    final.at[x, 'language'] = lang_string

    genre_string = ""
    for gen in genre:
        gen = gen['name']
        genre_string = str(genre_string) + str(gen) + ";"
    genre_string = genre_string[:-1]
    final.at[x, 'genre'] = genre_string

    country_string = ""
    for cou in country:
        cou = cou['name']
        country_string = str(country_string) + str(cou) + ";"
    country_string = country_string[:-1]
    final.at[x, 'country'] = country_string

    people = movie.credits()

    final = crew_cast (final,people,x)

    check = 'ok'
    return [check,final]

def episode_information_saving_0(final, x, tmdb_id, uri, rate, imdb_id, type, title, year):
    try:

        final.at[x, 'uri'] = uri
        final.at[x, 'imdb_id'] = imdb_id
        final.at[x, 'tmdb_id'] = tmdb_id
        final.at[x, 'title'] = title
        final.at[x, 'release'] = year
        # final.at[x, 'runtime'] = runtime
        # final.at[x, 'genre'] = genre
        final.at[x, 'type'] = type
        final.at[x, 'rate'] = rate
        check = 'ok'

    except:
        check = 0
        pass

    return [check, final]

def crew_cast (final,people,x):
    cast = people['cast']
    cast_string = ""
    for person in cast:
        person_id = person['id']
        #name = person['name']
        cast_string = str(cast_string) + str(person_id) + ";"
    cast_string = cast_string[:-1]
    final.at[x, 'cast'] = cast_string

    crew = people['crew']
    crew_string = ""
    for person in crew:
        person_id = person['id']
        role = person['department']
        #name = person['name']
        crew_string = str(crew_string) + str(person_id) + ":" + str(role) + ";"
    crew_string = crew_string[:-1]
    final.at[x, 'crew'] = crew_string
    return final

def person_op(id):
    person = tmdb.People(id=id)
    response = person.info()
    name = response['name']
    try:
        pic = person.images()
        pic = (pic['profiles'][0]['file_path'])
    except:
        pic = ""
    return [name, pic]