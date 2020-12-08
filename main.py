dict_operations = {
    0: "Construction/Updating of the general DB;",
    1: "Obtain stats;",
    2: "Refactor in IMDb (useful for Movielens);",
    3: "Affinity between two users;",
    4: "Exit"
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
            from tmdb import tmdb_py
            tmdb_py()
            from expand import expand
            expand()
        if filter == 1:
            dict_stats = {
                0: "Films viewed by year of release;",
                1: "Films viewed by year of viewing;",
                2: "Most frequent people in the database;",
                3: "Map;",
                4: "Back;",
                5: "Exit"
            }
            print("\nSTATS\nWhat do you want to do?")
            for n2 in dict_stats:
                print(str(n2) + " - " + str(dict_stats[n2]))
            filter2 = int(input())
            if filter2 == 0:
                try:
                    from stats import watched_by_release_year
                    watched_by_release_year()
                except:
                    print("\nError, check that you have built the main DB")
                    pass
            if filter2 == 1:
                try:
                    from stats import watched_by_year
                    watched_by_year()
                except:
                    print("\nError, check that you have built the main DB")
                    pass
            if filter2 == 2:
                try:
                    from stats import filtering_op,crew_count,cast_count
                    print("\nCrew Count...")
                    crew = crew_count()
                    print("\nCast Count...")
                    cast = cast_count()
                    print("\n")
                    filtering_op(cast, crew)
                except:
                    print("\nError, check that you have built the main DB")
                    pass
            if filter2 == 3:
                try:
                    from stats import movie_map, movie_country
                    db = movie_country()
                    movie_map(db)
                except:
                    print("\nError, check that you have built the main DB")
                    pass
            if filter2 == 4:
                menu()
            if filter2 == 5:
                break

        if filter == 3:
            try:
                from reformat_in_imdb import reformat_imdb
                reformat_imdb()
            except:
                print("\nError, check that you have built the main DB")
                pass

        if filter == 4:
            from affinity import affinity
            user1 = input("Enter first username: ")
            user2 = input("Enter second username: ")
            affinity(user1, user2)
            pass

        if filter == 5:
            break
            pass

menu()