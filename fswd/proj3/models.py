from google.appengine.ext import ndb

class Account(ndb.Model):
    '''
    Represents a user with an account to write blogs.

    Fields:
        id: The user name for the account.
        salt: The salt for the password for login cookies.
        psswdhash: The hash of the salt and the password.
    '''
    salt = ndb.IntegerProperty(required=True)
    psswdhash = ndb.StringProperty(required=True)

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
    blog = ndb.TextProperty(required=True, validator=check_str_not_empty)
    likes = ndb.KeyProperty(kind=Account, repeated=True)

    @property
    def tease(self):
        """Computes the tease of the blog."""
        MIN_TOKENS_IN_TEASE = 200
        MAX_TOKENS_IN_TEASE = 350
        if len(blog) < MIN_TOKENS_IN_TEASE:
            return blog
        index = MIN_TOKENS_IN_TEASE - 1
        space_index = 0
        found_dot = False
        # Try to parse full words, but not more than contain
        # MAX_TOKENS_IN_TEASE.
        while index < len(blog) and index < MAX_TOKENS_IN_TEASE:
            c = blog[index]
            if c.isspace():
                space_index = index
            if c == '.':
                found_dot = True
                break
            index += 1
        if found_dot:
            return blog[::index]
        if space_index:
            return blog[::space_index].rstrip()
        if MAX_TOKENS_IN_TEASE > len(blog):
            return blog
        return blog[::MAX_TOKENS_IN_TEASE].rstrip()

class BlogComment(ndb.Model):
    '''
    A blog commment.

    Fields:
        blog: The key property of the blog for which this is a comment.
        user: The user who posted this comment.
        date: The date-time the comment was posted.
        comment: The comment.
    '''
    blog = ndb.KeyProperty(required=True)
    user = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(required=True, auto_now_add=True)
    comment = ndb.TextProperty(required=True, validator=check_str_not_empty)

def check_str_not_empty(prop, content):
    """Returns a datastore_errors.BadValueError if the string value of a Text
    or String property is empty.

    Args:
        prop: The ndb property type.
        val: The blog content.
    """
    if not content.strip(): raise datastore_erros.BadValueError
    return content
