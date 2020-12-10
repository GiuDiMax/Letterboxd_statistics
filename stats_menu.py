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

            print("\nCrew Count...")
            crew = crew_count(db)
            print("\nCast Count...")
            cast = cast_count(db)
            print("\n")
            filtering_op(cast, crew, 10)
        except:
            print("\nError, check that you have built the main DB")
            pass
    if filter2 == 4:
        try:
            from stats import filtering_op_avg, cast_rate, crew_rate

            print("\nCrew Count...")
            crew = crew_rate(db)
            print("\nCast Count...")
            cast = cast_rate(db)
            print("\n")
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

def stats_menu2(db, watched, diary):

    dict_stats = {
        0: "General stats",
        1: "Films viewed by year of release;",
        2: "Most frequent people in the database;",
        3: "Most liked people in the database;",
        4: "Map;",
        5: "Back.",
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
            from stats import filtering_op, crew_count, cast_count

            print("\nCrew Count...")
            crew = crew_count(db)
            print("\nCast Count...")
            cast = cast_count(db)
            print("\n")
            filtering_op(cast, crew, 5)
        except:
            print("\nError, check that you have built the main DB")
            pass
    if filter2 == 3:
        try:
            from stats import filtering_op_avg, cast_rate, crew_rate

            print("\nCrew Count...")
            crew = crew_rate(db)
            print("\nCast Count...")
            cast = cast_rate(db)
            print("\n")
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