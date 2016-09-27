import datetime
import jinja2
import os
import webapp2

from google.appengine.api import users

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('hello from om-blog')

application = webapp2.WSGIApplication([('/', MainPage)], debug=True)
