#!/usr/bin/env python
import webbrowser

INFO_NA = 'Information Not Available'

class Movie():
    def __init__(self, fields):
	self.title = fields.get('Title', INFO_NA)
	self.plot = fields.get('Plot', INFO_NA)
	self.url_poster = fields.get('Poster', INFO_NA)
	self.url_trailer = fields.get('Trailer', INFO_NA)
	self.rating = fields.get('Rated', INFO_NA)
	self.writer = fields.get('Writer', INFO_NA)
	self.imdb_rating = fields.get('imdbRating', INFO_NA)
	self.director = fields.get('Director', INFO_NA)
	self.release_year = fields.get('Year', INFO_NA)
	self.genre = fields.get('Genre', INFO_NA)
	self.awards = fields.get('Awards', INFO_NA)
    def show_trailer(self):
	webbrowser.open(self.url_trailer)
