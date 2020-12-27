import tmdbsimple as tmdb
from config import tmdb_api
tmdb.API_KEY = tmdb_api

def serie_information_saving(final,x,tmdb_id,uri,rate,imdb_id, type, watched, rewatch):
    try:
        serie = tmdb.TV(tmdb_id)
        response = serie.info()

        #imdb_id = response['imdb_id']
        tmdb_id = response['id']
        title = response['name']
        release = response['first_air_date']
        from web_scraping import obtain_runtime
        runtime = obtain_runtime(uri)
        genre = response['genres']
        language = response['spoken_languages']
        country = response['production_countries']
        studios = response['production_companies']

        final.at[x, 'uri'] = uri
        final.at[x, 'imdb_id'] = imdb_id
        final.at[x, 'tmdb_id'] = tmdb_id
        final.at[x, 'title'] = title
        final.at[x, 'release'] = release
        final.at[x, 'runtime'] = runtime
        final.at[x, 'type'] = type
        final.at[x, 'rate'] = rate
        final.at[x, 'watched'] = watched
        final.at[x, 'rewatch'] = rewatch

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
            cou = cou['iso_3166_1']
            country_string = str(country_string) + str(cou) + ";"
        country_string = country_string[:-1]
        final.at[x, 'country'] = country_string

        studios_string = ""
        for stu in studios:
            stu = stu['name']
            studios_string = str(studios_string) + str(stu) + ";"
        studios_string = studios_string[:-1]
        final.at[x, 'studios'] = studios_string

        people = serie.credits()
        final = crew_cast(final, people, x)

        check = 'ok'

    except:
        check = 0
        pass

    return[check,final]

def movie_information_saving(final,x,id,uri,rate, watched, rewatch):
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
    studios = response['production_companies']
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
    final.at[x,'watched'] = watched
    final.at[x,'rewatch'] = rewatch

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
        cou = cou['iso_3166_1']
        country_string = str(country_string) + str(cou) + ";"
    country_string = country_string[:-1]
    final.at[x, 'country'] = country_string

    studios_string = ""
    for stu in studios:
        stu = stu['name']
        studios_string = str(studios_string) + str(stu) + ";"
    studios_string = studios_string[:-1]
    final.at[x, 'studios'] = studios_string

    people = movie.credits()

    final = crew_cast (final,people,x)

    check = 'ok'
    return [check,final]

def generic_information_saving(final, x, tmdb_id, uri, rate, imdb_id, type, title, year, watched, rewatch):
    try:

        final.at[x, 'uri'] = uri
        final.at[x, 'imdb_id'] = imdb_id
        final.at[x, 'tmdb_id'] = tmdb_id
        final.at[x, 'title'] = title
        final.at[x, 'release'] = year
        # final.at[x, 'genre'] = genre
        from web_scraping import obtain_runtime
        try:
            runtime = obtain_runtime(uri)
            final.at[x, 'runtime'] = runtime
        except:
            pass
        final.at[x, 'type'] = type
        final.at[x, 'rate'] = rate
        final.at[x, 'watched'] = watched
        final.at[x, 'rewatch'] = rewatch
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
        name = person['name']
        cast_string = str(cast_string) + str(person_id) + ":" + str(name) + ";"
    cast_string = cast_string[:-1]
    final.at[x, 'cast'] = cast_string

    crew = people['crew']
    crew_string = ""
    for person in crew:
        person_id = person['id']
        role = person['job']
        name = person['name']
        if role in ['Director','Producer','Writer','Editor',
                    'Director of Photography'
                    '''
                    'Sound','Production Designer',
                    'Art Direction','Set Decoration','Visual Effects',
                    'Original Music Composer','Sound','Costume Design',
                    'Makeup Department Head'
                    '''
                    ]:
            crew_string = str(crew_string) + str(person_id) + ":" + str(role) + ":" + str(name) + ";"
        else:
            pass
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