#!/usr/bin/env python

import urllib
import re

# Idea is taken from the following article:
# http://www.codeproject.com/Articles/873060/Python-Search-Youtube-for-Video

RE_STR = r'href=\"\/watch\?v=(.{11})'
SEARCH_FMT = 'http://www.youtube.com/results?search_query=%s'
VIDEO_FMT = 'http://www.youtube.com/watch?v=%s'

def get_trailer_url(movie):
    '''
    Searches Youtube for a movie trailer.

    Args:
        movie: The name of the movie to search for. Cannot be empty.
    Return:
        A URL for the movie trailer. 
    '''
    if not movie: raise ValueError("Movie title cannot be empty")
    search = urllib.quote(movie.strip() + ' movie trailer')
    content = urllib.urlopen(SEARCH_FMT % search)
    search_results = re.search(RE_STR, content.read())
    if not search_results: raise ValueError("Could not find URL")
    return VIDEO_FMT % search_results.group(1)
