from google.appengine.ext import ndb

class Account(ndb.Model):
    user = ndb.StringProperty()
    password = ndb.StringProperty()

class Blog(ndb.Model):
    user = ndb.StringProperty()
    date = ndb.StringProperty()
    blog = ndb.TextProperty()
    likes = ndb.IntegerProperty()

class LikesTable(ndb.Model):
    blogkey = ndb.StringProperty()
    user = ndb.StringProperty()
