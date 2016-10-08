from google.appengine.ext import ndb

class Account(ndb.Model):
    '''
    Represents a user with an account to write blogs.

    Fields:
        id: The user name for the account.
        password: The password for the account.
    '''
    password = ndb.StringProperty(required=True)

class Blog(ndb.Model):
    '''
    Represents a blog entry.

    Fields:
        user: The blog author.
        date: The date created.
        blog: The blog content.
        likes: The number of like votes.
    '''
    user = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(required=True)
    blog = ndb.TextProperty(required=True)
    likes = ndb.KeyProperty(repeat=True)
