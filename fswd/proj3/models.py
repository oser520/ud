from google.appengine.ext import ndb

class Account(ndb.Model):
    user = ndb.StringProperty()
    password = ndb.StringProperty()

class Blog(ndb.Model):
    user = ndb.StringProperty()
    date = ndb.DateTimeProperty()
    blog = ndb.TextProperty()
    likes = ndb.IntegerProperty()

class LikesTable(ndb.Model):
    blogkey = ndb.KeyProperty(kind=Blog)
    user = ndb.StringProperty()
