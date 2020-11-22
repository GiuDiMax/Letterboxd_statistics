from urllib.request import urlopen
import tmdbsimple as tmdb

def tmdb_id_scraping(url):
    # page = requests.get(url)
    page = urlopen(url)

    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    start_index = html.find('www.themoviedb.org/') + len('www.themoviedb.org/')
    title = html[start_index:start_index+10]
    title = str.split(title, '/')
    type = title[0]
    title = title[1]
    return [type, title]

def imdb_id_scraping(url):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    start_index = html.find('http://www.imdb.com/title/') + len('http://www.imdb.com/title/')
    title = html[start_index:start_index+20]
    title = str.split(title, '/')
    title = title[0]
    return(title)

def imdb_episode_scraping(imdb_id):
    url = 'https://www.imdb.com/title/' + str(imdb_id) + "/"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    start_index = html.find("<title>")
    end_index = html.find("</title>")
    title_serie = html[start_index + 13:end_index]
    title_serie = str.split(title_serie, "&")
    title_serie = title_serie[0]

    start_index = html.find('Season ')
    tot = html[start_index:start_index + 50]
    tot = str.split(tot, " ")
    numeric_filter = filter(str.isdigit, tot[1])
    season = "".join(numeric_filter)
    numeric_filter = filter(str.isdigit, tot[5])
    episode = "".join(numeric_filter)
    return [title_serie,season,episode]

def imdb_to_tmdb_id (imdb):
    list = tmdb.Find(imdb)
    list = list.info(external_source='imdb_id')
    id = 0
    type = 0
    for response in list:
        if list[response] != []:
            type = response[:-8]
            id = list[response]
            id = id[0]['id']
            break
    return[id, type]