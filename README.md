# Letterboxd statistics
Get stats from your letterboxd export zip file.

## Language
- This project is in Italian in some part, sorry.

## Usage
- Install requirements.txt;
- Write your TMDB API key in config file, to obtain it follow this guide: https://developers.themoviedb.org/3/getting-started/introduction;
- Move file downlaoded from https://letterboxd.com/settings/data/ in input folder;
- Run main.py.

## Bugs
- TV episodes are not scraped;
- TV shows don't have runtime;
- Ratings are not updated if they change.

## Future developments
- Reduce the number of people in "Crew", to optimize time and statistics;
- Most liked Cast/Crew by avg ratings;
- Filtering per year;
- Map of nations.
