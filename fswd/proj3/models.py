from google.appengine.ext import ndb

class Account(ndb.Model):
    '''
    Represents a user with an account to write blogs.

    Fields:
        user: The user name for the account.
        password: The password for the account.
    '''
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
