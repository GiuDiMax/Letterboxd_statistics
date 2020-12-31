import pandas as pd

def reformat_imdb():
    film = pd.read_csv("output/lbd_scrap.csv")

    film = film[film.imdb != 'tt0000000']
    film = film[film.imdb != '']
    film = film[film.rate != '']
    film = film[['imdb', 'rate']]

    film['Const'] = film['imdb']
    film = film.dropna()
    film['Your Rating'] = (film['rate'] * 2).astype(int)

    film['Date Rated'] = '2019-01-01'
    film['Title'] = 'NoTitle'
    film['URL'] = 'https://www.imdb.com/title/tt000000/'
    film['Title Type'] = 'movie'
    film['IMDb Rating'] = '6'
    film['Runtime (mins)'] = '120'
    film['Year'] = '2019'
    film['Genres'] = 'A,B'
    film['Num Votes'] = '999999'
    film['Release Date'] = '2019-01-01'
    film['Directors'] = 'NoOne'

    imdb = film[['Const', 'Your Rating', 'Date Rated', 'Title', 'URL', 'Title Type',
                 'IMDb Rating', 'Runtime (mins)', 'Year', 'Genres', 'Num Votes',
                 'Release Date', 'Directors']]

    imdb.to_csv(r'output/imdb_ratings.csv', index=False, header=True)
    print("File saved in output/imdb_ratings")