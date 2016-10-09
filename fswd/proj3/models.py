from google.appengine.ext import ndb

class Account(ndb.Model):
    '''
    Represents a user with an account to write blogs.

    Fields:
        id: The user name for the account.
        password: The password for the account.
        salt: The salt for the password for login cookies.
    '''
    password = ndb.StringProperty(required=True)
    salt = ndb.IntegerProperty(required=True)

class Blog(ndb.Model):
    '''
    Represents a blog entry.

    Fields:
        id: Concatenation of Account.id, blog title, and datetime blog is
            created, i.e., Account.id-title-datetime.
        user: The blog author.
        title: The blog title.
        date: The date-time the blog was created.
        blog: The blog content.
        likes: The number of like votes.
    '''
    user = ndb.StringProperty(required=True)
    title = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(required=True, auto_now_add=True)
    blog = ndb.TextProperty(required=True, validator=check_blog_entry)
    likes = ndb.KeyProperty(kind=Account, repeated=True)

def check_blog_entry(prop, content):
    """Verifies that the blog entry contains content.

    If the blog entry contains content, the content if returned, otherwise a
    datastore_errors.BadValueError is returned.

    Args:
        prop: The ndb property type.
        val: The blog content.
    """
    if not content.strip(): raise datastore_erros.BadValueError
    return content
