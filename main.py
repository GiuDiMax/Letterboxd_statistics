dict_operations = {
    0: "Construction/Updating of the general DB;",
    1: "Obtain all-time stats;",
    2: "Stats for a specific year;",
    3: "Stats for a specific release year; (future update)",
    4: "Refactor in IMDb (useful for Movielens);",
    5: "Affinity between two users;",
    6: "Exit"
}

def menu():
    filter = 5
    while int(filter) != 4:
        print("\nWhat do you want to do?")
        for n in dict_operations:
            print(str(n) + " - " + str(dict_operations[n]))
        filter = input()
        try:
            filter = int(filter)
        except:
            print("Error")
        if filter == 0:
            from join_letterboxd_file import join_letterboxd
            join_letterboxd()
            from lbd import letterboxd
            letterboxd()
            from expand import expand
            expand()
        if filter == 1:
            from stats_menu import stats_menu
            import pandas as pd

            db = pd.read_csv("output/database.csv", low_memory=False)
            db = pd.DataFrame(db)

            diary = pd.read_csv("input/diary.csv")
            diary = pd.DataFrame(diary)
            diary = diary['Watched Date'].str.split("-", expand=True)
            diary = (diary.iloc[:, 0])

            watched = pd.read_csv("input/watched.csv")
            watched = pd.DataFrame(watched)

            stats_menu(db, watched, diary)

        if filter == 2:
            year_filter = input("\nWhat year? ")

            from stats_menu import stats_menu_watching
            import pandas as pd

            diary = pd.read_csv("input/diary.csv")
            diary = pd.DataFrame(diary)
            diary = diary[diary['Watched Date'].str.startswith(year_filter)]
            #diary = (diary.iloc[:, 0])

            watched = pd.read_csv("input/watched.csv")
            watched = pd.DataFrame(watched)

            db2 = pd.merge(diary,watched,on=['Name','Year'])
            watched = db2[['Date_x', 'Name', 'Year', 'Letterboxd URI_y']]
            watched.columns=['Date', 'Name', 'Year', 'Letterboxd URI']

            db = pd.read_csv("output/database.csv", low_memory=False)
            db = pd.DataFrame(db)
            db = db[db['watched'].notna()]
            db = db[db['watched'].str.startswith(year_filter)]
            stats_menu_watching(db, watched, diary, year_filter)

        if filter == 3:
            year_filter = input("\nWhat year? ")

            from stats_menu import stats_menu_release
            import pandas as pd

            db = pd.read_csv("output/database.csv", low_memory=False)
            db = pd.DataFrame(db)
            db = db[db['year'].notna()]
            db = db[db['year'].str.startswith(year_filter)]

            diary = pd.read_csv("input/diary.csv")
            diary = pd.DataFrame(diary)
            diary = diary[diary['Watched Date'].str.startswith(year_filter)]
            watched = pd.read_csv("input/watched.csv")
            watched = pd.DataFrame(watched)

            stats_menu_release(db, watched, diary)

        if filter == 4:
            try:
                from reformat_in_imdb import reformat_imdb
                reformat_imdb()
            except:
                print("\nError, check that you have built the main DB")
                pass

        if filter == 5:
            from affinity import affinity
            user1 = input("Enter first username: ")
            user2 = input("Enter second username: ")
            affinity(user1, user2)
            pass

        if filter == 6:
            break
            pass

menu()