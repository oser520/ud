#!/usr/bin/env python

import argparse
import shelve
import sys
import time
import fresh_tomatoes
from media import Movie
from omdb import get_movie_info
from youtube_trailer import get_trailer_url

# default movies to search for and add to the movie trailer page
movie_titles = [
    'inception', 'braveheart', 'jason bourne', 'iron man',
    'g.i. jane', 'good will hunting', 'ray', 'furious 7',
    'san andreas', 'get shorty', 'lost in translation',
    'her', 'adaptation'
]

# parse the arguments
parser = argparse.ArgumentParser(description='Create Fresh Tomatoes Web Page')
parser.add_argument('--dbfile', default='movie_trailer_db',
    help='The database for the movie trailers')
parser.add_argument('-f', '--file',
    help='Input file to get movie titles from, with one title per line')
parser.add_argument('-l', '--list',
    help='List of movies separated by separator')
parser.add_argument('-s', '--separator', default=',',
    help='The separator used if a list of movies is provided')
args = parser.parse_args()

# open the database
db = shelve.open(args.dbfile, writeback=True)

# read titles from a file
if args.file:
    for title in open(args.file).readlines():
        title = title.strip().lower()
        movie_titles.append(title) if title

# process titles in list
if args.list:
    titles = args.list.split(args.separator)
    for title in titles:
        title = title.strip().lower()
        movie_titles.append(title) if title

# list of movies to include in trailer web page
movies = []

# process each movie title
for title in movie_titles:
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
