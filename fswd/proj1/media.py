#!/usr/bin/env python
import webbrowser

class Movie():
    def __init__(self, title):
	self.title = title
	self.plot = None
	self.url_poster = None
	self.url_trailer = None
	self.rating = None
	self.writer = None
	self.imdb_rating = None
	self.director = None
	self.release_year = None
	self.genre = None
	self.awards = None
    def show_trailer(self):
	webbrowser.open(self.url_trailer)
