import datetime
import jinja2
import os
import webapp2
import util
import models
import hmac
from google.appengine.ext import ndb

class BlogItem():
    """An item with basic info about a blog, including the title, author, date
    published, the number of likes it has, and the first few sentences of the
    blog.
    """
    def __init__(self, title, user, date, likes, intro):
        """Initializes a blog item.

        Args:
            title: The blog's title.
            user: The blog's author.
            date: The date published.
            likes: The number of people who like the blog.
            intro: The first few sentences of the blog.

        TODO: Use the datastore models to initialize these variables.
        """
        self.title = title
        self.user = user
        self.date = date
        self.likes = likes
        self.intro = intro

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

class MainPage(webapp2.RequestHandler):
    """Handle requests to the main blog site."""
    def get(self):
        # Get session status
        logged_status = util.is_session_req(self.request)
        # TODO: if logged_status[0] is true and logged_status[1] is false,
        # then do something to clear cookies
        template = template_env.get_template('content.html')
        blog_titles = []
        title = 'This is my blog title'
        user = 'om'
        date = datetime.datetime.now()
        likes = 111
        intro = '''
            This is the first sentence of the blog.
            This is the second sentence of the blog.
            This is the 3rd sentence of the blog.
            '''
        for _ in range(20):
            item = BlogItem(title, user, date, likes, intro)
            blog_titles.append(item)
        context = {
            'blog_titles': blog_titles,
            'loggedin': 'Login'
        }
        self.response.out.write(template.render(context))

class LoginPage(webapp2.RequestHandler):
    """Handle requests to login as a user of the blog site."""
    def get(self):
        """Render the login page."""
        # TODO: get username and password from form and login user to system
        template = template_env.get_template('login.html')
        self.response.out.write(template.render())

class DoLoginPage(webapp2.RequestHandler):
    """Handle requests to login as a user of the blog site."""
    def post(self):
        """Verifies the user is registered.

        If the user is registered, then he is redirected to the main page,
        otherwise the user gets an error message indicating either the username
        does not exist, or the password is incorrect.

        TODO: implement
        """
        user = self.request.get('user')
        if not user:
            # TODO: return to login page, but hightlight input box and list
            # requirements for a valid user name
            self.response.out.write('Error: The username cannot be empty\n')
            return
        pwd = self.request.get('password')
        if not pwd:
            # TODO: return to login page with error for missing password
            self.response.out.write('Error: The password name cannot be empty\n')
            return
        self.response.out.write('Hello %s\nI have your password %s\n' % (user, pwd))

class RegisterPage(webapp2.RequestHandler):
    """Handle requests to register as a user of the blog site."""
    def get(self):
        """Render the registration page."""
        template = template_env.get_template('register.html')
        self.response.out.write(template.render())

class DoRegisterPage(webapp2.RequestHandler):
    """Handle requests to register as a user of the blog site."""
    def post(self):
        """Registers a user.

        Checks the username and password are valid, and the username is not
        taken. If the username is taken, then the user is prompted for another
        username. The user is redirected to the main blog page after
        registration is complete.

        TODO: implement
        """
        # Validate username
        user = self.request.get('user')
        user = util.process_username(user)
        if not user:
            # TODO: redirect to register page, but highlight username input
            # and specify requirements.
            s = 'Error: The username %s is not valid\n'
            self.response.out.write(s % user)
            return
        # Check that username doesn't already exist
        account = models.Account.get_by_id(user)
        if account:
            # TODO: redirect to register page, but highlight username input
            s = 'Error: The username %s already exists\n'
            self.response.out.write(s % user)
            return
        # Validate password
        pwd = self.request.get('password')
        if not util.process_password(pwd):
            # TODO: redirect to register page, but highlight password input
            # and specify requirements.
            self.response.out.write('Error: The password is not valid\n')
            return
        # Create account
        salt = util.gensalt()
        hsh = util.gethsh(salt, pwd)
        account = models.Account(id=user, salt=salt, psswdhash=hsh)
        try:
            account.put()
        except ndb.TransactionFailedError:
            s = 'Error: Unable to create account. Please try again.'
            self.response.out.write(s)
            return
        # set session cookies
        # TODO: implement correctly
        self.response.set_cookie('name', user)
        self.response.set_cookie('secret', hsh)
        # Redirect to main page with full access
        self.redirect('/')

# TODO: create a signout handler that handles a user's request to sign out
# This handler should clear the cookies and redirect the user to the main
# blog page.

# TODO: create a request handler to compose a blog - only for users who are logged in

# TODO: create a request handler to save a blog

# TODO: create a request handler to write a comment on a blog

# TODO: create a request handler to edit a blog

# TODO: create a request handler to delete a blog

handlers = [
    ('/', MainPage),
    ('/login', LoginPage),
    ('/do-login', DoLoginPage),
    ('/register', RegisterPage),
    ('/do-register', DoRegisterPage),
]
application = webapp2.WSGIApplication(handlers, debug=True)
