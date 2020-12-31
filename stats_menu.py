def stats_menu(db, watched, diary):

    dict_stats = {
        0: "General stats",
        1: "Films viewed by year of release;",
        2: "Films viewed by year of viewing;",
        3: "Most frequent people in the database;",
        4: "Most liked people in the database;",
        5: "Map;",
        6: "Back;",
        7: "Exit"
    }

    filter2 = 0
    while filter2 != 8:
        print("\nSTATS\nWhat do you want to do?")
        for n2 in dict_stats:
            print(str(n2) + " - " + str(dict_stats[n2]))
        filter2 = int(input())

        if filter2 == 0:
            from stats import general
            general(db)

        if filter2 == 1:
            try:
                from stats import watched_by_release_year
                watched_by_release_year(watched)
            except:
                print("\nError, check that you have built the main DB")
                pass
        if filter2 == 2:
            try:
                from stats import watched_by_year
                watched_by_year(diary)
            except:
                print("\nError, check that you have built the main DB")
                pass
        if filter2 == 3:
            try:
                from stats import people_count
                people_count(db, 10)
            except:
                print("\nError, check that you have built the main DB")
                pass
        if filter2 == 4:
            try:
                from stats import people_top_count
                people_top_count(db, 10)
            except:
                print("\nError, check that you have built the main DB")
                pass
        if filter2 == 5:
            try:
                from stats import movie_map, movie_country
                movie_map(db)
            except:
                print("\nError, check that you have built the main DB")
                pass
        if filter2 == 6:
            from main import menu
            menu()
        if filter2 == 7:
            exit()

def stats_menu_watching(db, watched, diary, year):

    dict_stats = {
        0: "General stats",
        1: "Films viewed by year of release;",
        2: "Most frequent people of the year;",
        3: "Most liked people of the year;",
        4: "Map;",
        5: "Back;",
        6: "Exit"
    }

    filter2 = 0
    while filter2 != 8:
        print("\nSTATS\nWhat do you want to do?")
        for n2 in dict_stats:
            print(str(n2) + " - " + str(dict_stats[n2]))
        filter2 = int(input())

        if filter2 == 0:
            from stats import general_year
            general_year(db, year)

        if filter2 == 1:
            try:
                from stats import watched_by_release_year
                watched_by_release_year(watched)
            except:
                print("\nError, check that you have built the main DB")
                pass
        if filter2 == 2:
            try:
                from stats import people_count
                people_count(db, 5)
            except:
                print("\nError, check that you have built the main DB")
                pass
        if filter2 == 3:
            try:
                from stats import people_top_count
                people_top_count(db, 5)
            except:
                print("\nError, check that you have built the main DB")
                pass
        if filter2 == 4:
            try:
                from stats import movie_map, movie_country
                movie_map(db)
            except:
                print("\nError, check that you have built the main DB")
                pass
        if filter2 == 5:
            from main import menu
            menu()
        if filter2 == 6:
            exit()

def stats_menu_release(db, watched, diary):

    dict_stats = {
        0: "General stats",
        1: "Films viewed by year of viewing;",
        2: "Most frequent people in the database;",
        3: "Most liked people in the database;",
        4: "Map;",
        5: "Back;",
        6: "Exit"
    }

    filter2 = 0
    while filter2 != 8:
        print("\nSTATS\nWhat do you want to do?")
        for n2 in dict_stats:
            print(str(n2) + " - " + str(dict_stats[n2]))
        filter2 = int(input())

        if filter2 == 0:
            from stats import general
            general(db)

        if filter2 == 1:
            try:
                from stats import watched_by_year
                watched_by_year(diary)
            except:
                print("\nError, check that you have built the main DB")
                pass
        if filter2 == 2:
            try:
                from stats import people_count
                people_count(db, 10)
            except:
                print("\nError, check that you have built the main DB")
                pass
        if filter2 == 3:
            try:
                from stats import people_top_count
                people_top_count(db, 10)
            except:
                print("\nError, check that you have built the main DB")
                pass
        if filter2 == 4:
            try:
                from stats import movie_map, movie_country
                movie_map(db)
            except:
                print("\nError, check that you have built the main DB")
                pass
        if filter2 == 5:
            from main import menu
            menu()
        if filter2 == 6:
            exit()