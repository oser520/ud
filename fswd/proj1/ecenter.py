#!/usr/bin/env python

from media import Movie
from omdb import get_movie_info
from youtube_trailer import get_trailer_url
import fresh_tomatoes
import time
import sys

'''
movie_titles = [
    'inception', 'braveheart', 'adaptation', 'jason bourne',
    'g.i. jane', 'good will hunting', 'ray', 'furious 7',
    'san andreas', 'get shorty', 'lost in translation', 'her'
]
'''
movie_titles = ['batman vs superman', 'avengers', 'star trek']

movies = []

for title in movie_titles:
    movie_details = get_movie_info(title)
    found_details = movie_details.get('Response', 'False') == 'True'
    if not found_details:
        sys.stderr.write('Movie %s not found in OMDB\n' % title)
    else:
        print "Found details for movie %s" % title
        movie = Movie(movie_details)
        movie.url_trailer = get_trailer_url(movie.title)
        print "Found trailer URL for movie %s" % title
        print
        movies.append(movie)
    time.sleep(1)

fresh_tomatoes.open_movies_page(movies)

sys.exit(0)
