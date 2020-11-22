import tmdbsimple as tmdb
from gettinginfo_tmdb import *

tmdb.API_KEY = '6fff7e293df6a808b97101a26c86a545'

'''
x = x + 1
check = 0
imdb_id = 0
uri = row['uri']
rate = row['Rating']
title2 = row['Name']
year2 = row['Year']
'''

title2 = 'The Hunt'
year2 = '2012'
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
        movie = tmdb.Movies(id)
        response = movie.info()
        tmdb_id = response['id']

except:
    check = 0
    pass
