from urllib.request import urlopen
import tmdbsimple as tmdb
import requests
from bs4 import BeautifulSoup
import pandas as pd

def list_user(user):
    gen_url = 'https://letterboxd.com/'
    page_url = '/films/page/'
    num = '1'
    url = gen_url + user + page_url + num
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='content')
    results = results.find('section', class_='section col-main overflow')
    results = results.find('div', class_='pagination')
    results = results.find('div', class_='paginate-pages')
    results = results.find_all('li', class_='paginate-page')
    results = str(results[-1])
    num_pages = int(results.split("/page/", 1)[1].split("/", 1)[0])

    rates = pd.DataFrame([{'id': 0, 'name': 'ciao', 'rate': 0, 'like': 0}])
    rates = rates.drop([0])
    x = -1

    for i in range(num_pages):
        i = i + 1
        num = str(i)
        url = gen_url + user + page_url + num
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='content')
        results = results.find('section', class_='section col-main overflow')
        results = results.find('ul', class_='poster-list -p70 -grid film-list clear')
        results = results.find_all('li', class_='poster-container')
        for result in results:
            x = x + 1

            try:
                rateelike = result.find_all('span')
                rate = int(str(rateelike[2]).split('rated-', 1)[1].split('"', 1)[0])
            except:
                rate = int(0)
            try:
                like = rateelike[3]
                like = 1
            except:
                like = 0

            name = str(result.find('img', class_="image"))
            name = name.split('"', 2)[1]
            id = str(result)
            id = int(id.split('data-film-id=', 1)[1].split('"', 2)[1])
            rates.at[x, 'id'] = id
            rates.at[x, 'rate'] = rate
            rates.at[x, 'like'] = like
            rates.at[x, 'name'] = name

    rates["id"] = rates["id"].astype(int)
    rates["rate"] = rates["rate"].astype(int)
    rates["like"] = rates["like"].astype(int)
    return(rates)

def affinity(user1, user2):
    print("Start the analysis...")
    #print("Building list for user: " + str(user1))
    list1 = list_user(user1)
    #print("Building list for user: " + str(user2))
    list2 = list_user(user2)
    #print("Start the analysis...")
    list = pd.merge(list1, list2, on=['id','name'])
    list['aff'] = 0
    list['meanrate'] = 0.0
    num_titoli_comune = int(len(list))
    bonus_count = 0
    for x in range(num_titoli_comune):
        bonus = 0
        rate1 = int(list.at[x,'rate_x'])
        rate2 = int(list.at[x,'rate_y'])
        like1 = int(list.at[x,'like_x'])
        like2 = int(list.at[x, 'like_y'])
        if rate1 == 0 or rate2 == 0:
            list.at[x,'aff'] = 0
        else:
            if like1 == 1 and like2 == 1:
                bonus_count = bonus_count+1
                bonus = 1.1
            else:
                bonus = 1
            list.at[x,'aff'] = (100 - abs(rate1-rate2)*11)*bonus
            list.at[x, 'meanrate'] = (rate1+rate2)/2

    list = list[list.aff != 0]
    affinityper = list['aff'].mean(axis=0)
    print("\n")
    print("Users: "+str(user1) +" & "+str(user2))
    print("AFFINITY = " + str(round(affinityper,2)) +" %")
    print("Titles SEEN by both = "+str(num_titoli_comune))
    print("Titles VOTED by both = "+str(len(list)))
    print("Titles LIKED by both = " + str(bonus_count))
    meanrate = list.sort_values(by=['meanrate','aff','like_x','like_y'],ascending=False).head(20)
    meanrate = meanrate.reset_index()
    print("\nMOST RATED titles:\n")
    for k in range(10):
        likeprint = ""
        if meanrate.at[k,'like_x'] == 1 and meanrate.at[k,'like_x'] == 1:
            likeprint = ' ❤'
        print(str(meanrate.at[k,'name'])+"\t"+str(meanrate.at[k,'meanrate'])+str(likeprint))
