import urllib

def get_movie_info(title):
    '''
    Searches the Open Movie Database for basic movie information for a given
    title.

    Args:
        title: The name of the movie to search for. It cannot be empty.
    Return:
        A JSON string representing the details of the movie, such as the title,
        or a failure response if the movie is not found.
    '''
    if not title:
        raise ValueError("title cannot be empty")
    title = urllib.quote(title)
    urlfmt = 'http://www.omdbapi.com/?t=%s&plot=full&r=json'
    return urllib.urlopen(urlfmt % title).read()
