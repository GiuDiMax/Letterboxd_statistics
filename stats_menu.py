def stats_menu(db, watched, diary):

    dict_stats = {
        0: "General stats",
        1: "Films viewed by year of release;",
        2: "Films viewed by year of viewing;",
        3: "Most frequent people in the database;",
        4: "Most liked people in the database;",
        5: "Map;",
        6: "Back."
    }

    print("\nSTATS\nWhat do you want to do?")
    for n2 in dict_stats:
        print(str(n2) + " - " + str(dict_stats[n2]))
    filter2 = int(input())
    if filter2 == 0:
        from stats import general
        general(db,diary)

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
            from stats import filtering_op, crew_count, cast_count
            crew = crew_count(db)
            cast = cast_count(db)
            filtering_op(cast, crew, 10)
        except:
            print("\nError, check that you have built the main DB")
            pass
    if filter2 == 4:
        try:
            from stats import filtering_op_avg, cast_rate, crew_rate
            crew = crew_rate(db)
            cast = cast_rate(db)
            filtering_op_avg(cast, crew, 10)
        except:
            print("\nError, check that you have built the main DB")
            pass
    if filter2 == 5:
        try:
            from stats import movie_map, movie_country

            db = movie_country(db)
            movie_map(db)
        except:
            print("\nError, check that you have built the main DB")
            pass
    if filter2 == 6:
        from main import menu
        menu()

def stats_menu2(db, watched, diary, year_filter):
    filter2 = 0
    while filter2 != 5:
        try:
            dict_stats = {
                0: "General stats",
                1: "Films viewed by year of release;",
                2: "Most frequent people in the year DB;",
                3: "Most liked people in the year DB;",
                4: "Map;",
                5: "Back.",
            }
            print("\nSTATS\nWhat do you want to do?")
            for n2 in dict_stats:
                print(str(n2) + " - " + str(dict_stats[n2]))
            filter2 = int(input())

            if filter2 == 0:
                try:
                    from stats import general
                    print("\nWatched " + str(len(db)) + " movies in " + str(year_filter))
                    db2 = db[db['release'].str.startswith(year_filter)]
                    percentage = int(((len(db2)) / (len(db))) * 100)
                    print("Watched " + str(len(db2)) + " " + str(year_filter) +
                          "'s movies (" + str(percentage) + "%) of total")
                    general(db, diary)

                except:
                    print("\nError, check that you have built the main DB")
                    pass

            if filter2 == 1:
                try:
                    from stats import watched_by_release_year
                    watched_by_release_year(watched)
                except:
                    print("\nError, check that you have built the main DB")
                    pass
            if filter2 == 2:
                try:
                    from stats import filtering_op, crew_count, cast_count

                    crew = crew_count(db)
                    cast = cast_count(db)
                    filtering_op(cast, crew, 5)
                except:
                    print("\nError, check that you have built the main DB")
                    pass
            if filter2 == 3:
                try:
                    from stats import filtering_op_avg, cast_rate, crew_rate

                    crew = crew_rate(db)
                    cast = cast_rate(db)
                    filtering_op_avg(cast, crew, 5)
                except:
                    print("\nError, check that you have built the main DB")
                    pass
            if filter2 == 4:
                try:
                    from stats import movie_map, movie_country

                    db = movie_country(db)
                    movie_map(db)
                except:
                    print("\nError, check that you have built the main DB")
                    pass
            if filter2 == 5:
                from main import menu
                menu()
        except:
            print("Error!")
            from main import menu
            menu()


def stats_menu3(db, year_filter):
    filter2 = 0
    while filter2 != 4:
        try:
            dict_stats = {
                0: "General stats",
                1: "Most frequent people in the year DB;",
                2: "Most liked people in the year DB;",
                3: "Map;",
                4: "Back.",
            }
            print("\nSTATS\nWhat do you want to do?")
            for n2 in dict_stats:
                print(str(n2) + " - " + str(dict_stats[n2]))
            filter2 = int(input())

            if filter2 == 0:
                try:
                    from stats import general
                    print("\nWatched " + str(len(db)) + " movies in " + str(year_filter))
                    db2 = db[db['release'].str.startswith(year_filter)]
                    percentage = int(((len(db2)) / (len(db))) * 100)
                    print("Watched " + str(len(db2)) + " " + str(year_filter) +
                          "'s movies (" + str(percentage) + "%) of total")
                    diary = 0
                    general(db, diary)

                except:
                    print("\nError, check that you have built the main DB")
                    pass

            if filter2 == 1:
                try:
                    from stats import filtering_op, crew_count, cast_count

                    crew = crew_count(db)
                    cast = cast_count(db)
                    filtering_op(cast, crew, 5)
                except:
                    print("\nError, check that you have built the main DB")
                    pass
            if filter2 == 2:
                try:
                    from stats import filtering_op_avg, cast_rate, crew_rate

                    crew = crew_rate(db)
                    cast = cast_rate(db)
                    filtering_op_avg(cast, crew, 5)
                except:
                    print("\nError, check that you have built the main DB")
                    pass
            if filter2 == 3:
                try:
                    from stats import movie_map, movie_country

                    db = movie_country(db)
                    movie_map(db)
                except:
                    print("\nError, check that you have built the main DB")
                    pass
            if filter2 == 4:
                from main import menu
                menu()
        except:
            print("Error!")
            from main import menu
            menu()


