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
    '''
    Represents a blog entry.

    Fields:
        user: The blog author.
        date: The date created.
        blog: The blog content.
        likes: The number of like votes.
    '''
    user = ndb.StringProperty()
    date = ndb.DateTimeProperty()
    blog = ndb.TextProperty()
    likes = ndb.IntegerProperty()

class LikesTable(ndb.Model):
    '''
    Represents a mapping between blogs and people who've liked them.

    Fields:
        blogkey: The datastore key for a given blog.
        user: A user who liked the blog.
    '''
    blogkey = ndb.KeyProperty(kind=Blog)
    user = ndb.StringProperty()
