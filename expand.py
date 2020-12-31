import pandas as pd

def expand():
    film = pd.read_csv("output/lbd_scrap.csv")
    categories = ['studio', 'country', 'language', 'genre', 'actor', 'director',
                  'producer', 'writer', 'editor', 'cinematography', 'production-design',
                  'art-direction', 'set-decoration', 'visual-effects', 'composer',
                  'sound', 'costumes', 'make-up', 'co-director']

    final = film
    for category in categories:
        general_list = (film[category]).astype(str)
        general_list = general_list.str.split(";", expand=True)
        for x in range(len(general_list.columns)):
            string = str(category) + str(x + 1)
            general_list = general_list.rename(columns={x: string})
        final = pd.concat([final, general_list], axis=1)

    final["uri"] = final["uri"].str.replace("https://boxd.it/", "")
    final = final.drop(columns=categories)
    final = final.fillna("")
    final = final.replace(['nan'], '')

    #print("File espanso e salvato col nome di database.csv")
    final.to_csv(r'output/database.csv', index=False, header=True)
    print("File expanded successfully")