#!/usr/bin/env python
import webbrowser

class Movie():
    def __init__(self, fields):
        fields = {k.encode('ascii','ignore'):v.encode('ascii','ignore')
                    for k,v in fields.iteritems()}
        self.found = fields.get('Response', 'False') == 'True'
        self.search_title = None
	self.title = fields.get('Title', None)
	self.plot = fields.get('Plot', None)
	self.url_poster = fields.get('Poster', None)
        if self.url_poster == 'N/A': self.url_poster = None
	self.url_trailer = None
	self.rating = fields.get('Rated', None)
	self.writer = fields.get('Writer', None)
	self.imdb_rating = fields.get('imdbRating', None)
	self.director = fields.get('Director', None)
	self.release_year = fields.get('Year', None)
	self.genre = fields.get('Genre', None)
	self.awards = fields.get('Awards', None)
	self.runtime = fields.get('Runtime', None)
    def show_trailer(self):
	webbrowser.open(self.url_trailer)
