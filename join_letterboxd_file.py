import pandas as pd
import os
from zipfile import ZipFile
from os import listdir
from os.path import isfile, join

for file in os.listdir("input/"):
    if file.endswith(".zip"):
        print("File to analyze: " + str(file) +"?")
        print("press enter if yes, otherwise type no")
        confirm = input()
        if confirm == "":
            nome_file = ("input/"+str(file))
            break

with ZipFile(nome_file, 'r') as zip:
    zip.extract('watched.csv','input/')
    zip.extract('ratings.csv', 'input/')
    zip.extract('diary.csv', 'input/')
    zip.extract('profile.csv', 'input/')
    print("Extraction ok")

film = pd.read_csv("input/watched.csv")
rate = pd.read_csv("input/ratings.csv")
#date = pd.read_csv("input/diary.csv")
profile = pd.read_csv("input/profile.csv")

rate.columns = ['Date','Name','Year','Letterboxd URI','Rating']
#date.columns = ['Date','Name','Year','Letterboxd URI','Rating','Rewatch','Tags','Watched Date']
film.columns = ['Date','Name','Year','Letterboxd URI']

rate = rate[['Letterboxd URI','Rating']]

final = film.merge(rate, on='Letterboxd URI', how='left')

print("Join Complete!")
#filename = "output/prova/letterboxd_joined.csv"
#os.makedirs(os.path.dirname(filename), exist_ok=True)
final.to_csv (r'output/letterboxd_joined.csv', index = False, header=True)