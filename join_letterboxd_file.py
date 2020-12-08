def join_letterboxd():
    import pandas as pd
    import os
    from zipfile import ZipFile
    for file in os.listdir("input/"):
        if file.endswith(".zip"):
            print("File to analyze: " + str(file) + "?")
            print("press enter if yes, otherwise type no")
            confirm = input()
            if confirm == "":
                nome_file = ("input/" + str(file))
                break

    with ZipFile(nome_file, 'r') as zip:
        zip.extract('watched.csv', 'input/')
        zip.extract('ratings.csv', 'input/')
        zip.extract('diary.csv', 'input/')
        zip.extract('profile.csv', 'input/')
        print("Extraction ok")

    film = pd.read_csv("input/watched.csv")
    rate = pd.read_csv("input/ratings.csv")
    profile = pd.read_csv("input/profile.csv")

    rate.columns = ['Date', 'Name', 'Year', 'Letterboxd URI', 'Rating']
    film.columns = ['Date', 'Name', 'Year', 'Letterboxd URI']

    rate = rate[['Letterboxd URI', 'Rating']]

    final = film.merge(rate, on='Letterboxd URI', how='left')

    print("Join Complete!\n")
    final.to_csv(r'output/letterboxd_joined.csv', index=False, header=True)