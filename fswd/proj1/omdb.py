#!/usr/bin/env python
import urllib
import time
import json
import sys

def get_movie_info(title):
    '''
    Searches the Open Movie Database for basic movie information for a given
    title.

    Args:
        title: The name of the movie to search for. It cannot be empty.
    Return:
        A python dictionary representing a JSON response, which contains details
        of the movie, such as the title, and release date. If the title is not
        found, then a response contains an error message.
    Details:
        If the function is being invoked several times successively, then it may
        be a good idea to sleep before invoking the function, otherwise the OMDB
        server may not respond.
    '''
    if not title: raise ValueError('title cannot be empty')
    title = urllib.quote(title)
    urlfmt = 'http://www.omdbapi.com/?t=%s&plot=full&r=json'
    response = urllib.urlopen(urlfmt % title).read()
    return json.loads(response)

# Test get_movie_info() by sending requests for a few valid titles, one
# non-existing movie, and saving the responses to a log file. The output file
# should contain several valid responses with movie detains, and one should
# be an error reponse.
if __name__ == '__main__':
    movies = ['braveheart', 'jason bourne', 'inception',
    'a few good men', 'willywonka']
    test_out = open('test_get_movie_info.txt', 'w')
    for m in movies:
        test_out.write('Searching for movie: %s\n' % m)
        response = get_movie_info(m)
        movie_found = response.get('Response', 'False') == 'True'
        if movie_found:
            test_out.write('Movie %s found!\n' % m)
            test_out.write('The key=value pairs for %s are:\n' % m)
            for k,v in response.iteritems():
                test_out.write('\t%s=%s\n' % (k, v))
        else: test_out.write('Movie %s not found!\n' % m)
        test_out.write('Response:\n%s\n\n' % response)
        # sleep for one second to avoid hitting the omdb quickly
        time.sleep(1)
    sys.exit(0)
