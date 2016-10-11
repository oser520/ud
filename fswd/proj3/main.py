import datetime
import jinja2
import os
import webapp2
import util
import models

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
        # Get session cookies
        user = self.request.cookies.get('user')
        pwd = self.request.cookies.get('pwd')
        # TODO: use session cookies
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
            self.response.out.write('Error: The username cannot be empty\n')
        pwd = self.request.get('password')
        if not pwd:
            self.response.out.write('Error: The password name cannot be empty\n')
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
            s = 'Error: The username %s is not valid\n'
            self.response.out.write(s % user)
            return
        user = user.group()
        # Check that username doesn't already exist
        account = models.Account.get_by_id(user)
        if account:
            s = 'Error: The username %s already exists\n'
            self.response.out.write(s % user)
            return
        # Validate password
        pwd = self.request.get('password')
        if not util.process_password(pwd):
            self.response.out.write('Error: The password is not valid\n')
            return
        # Create account
        salt = util.create_salt()
        account = models.Account(id=user, password=pwd, salt=salt)
        try:
            account.put()
        except TransactionFailedError:
            s = 'Error: Unable to create account. Please try again.'
            self.response.out.write(s)
            return
        # set session cookies
        # TODO: implement correctly
        self.response.set_cookie('user', 'willy')
        self.response.set_cookie('pwd', 'weak')
        # Redirect to main page with full access
        self.redirect('/')

handlers = [
    ('/', MainPage),
    ('/login', LoginPage),
    ('/do-login', DoLoginPage),
    ('/register', RegisterPage),
    ('/do-register', DoRegisterPage),
]
application = webapp2.WSGIApplication(handlers, debug=True)
