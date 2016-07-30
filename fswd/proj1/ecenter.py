#!/usr/bin/env python

import shelve
from media import Movie
from omdb import get_movie_info
from youtube_trailer import get_trailer_url
import fresh_tomatoes
import time
import sys

# default movies to search for and add to the movie trailer page
movie_titles = [
    'inception', 'braveheart', 'jason bourne', 'iron man',
    'g.i. jane', 'good will hunting', 'ray', 'furious 7',
    'san andreas', 'get shorty', 'lost in translation',
    'her', 'adaptation'
]

# list of movies that don't contain any errors
movies = []

db = shelve.open('movie_trailer_db', writeback=True)

for title in movie_titles:
    title = title.lower()
    print 'Searching for movie %s' % title
    if db.has_key(title):
       print 'Movie %s found in database via search title' % title
       movies.append(db[title])
    else:
        response = get_movie_info(title)
        movie = Movie(response)
        if not movie.found:
            sys.stderr.write('Error: Movie %s not found in OMDB\n' % title)
            sys.stderr.write('Error: Response: %s\n' % response)
        elif not movie.url_poster:
            sys.stderr.write('Error: Movie %s does not contain a poster URL\n' % title)
            sys.stderr.write('Error: Response: %s\n' % response)
        else:
            print 'Found details for movie %s' % title
            if db.has_key(movie.title):
                print 'Movie %s found in database via OMDB title' % movie.title
                movie = db[movie.title]
            else:
                movie.search_title = title
                movie.url_trailer = get_trailer_url(movie.title)
                db[movie.title] = movie
                db[movie.search_title] = movie
            movies.append(movie)
        time.sleep(1)

db.close()
fresh_tomatoes.open_movies_page(movies)

sys.exit(0)
