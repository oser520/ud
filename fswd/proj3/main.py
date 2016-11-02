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

class MainHandler(webapp2.RequestHandler):
    """Handle requests to the main blog site."""
    def get(self):
        # Get session status
        logged_status = util.is_session_req(self.request)
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
            'loggedin': logged_status
        }
        self.response.out.write(template.render(context))

class LoginHandler(webapp2.RequestHandler):
    """Handle requests to login as a user of the blog site."""
    def get(self):
        """Render the login page."""
        # If the request is made as part of a session, then user has already signed in.
        if util.is_session_req(self.request):
            self.redirect('/')
            return

        # TODO: get username and password from form and login user to system
        template = template_env.get_template('login.html')
        self.response.out.write(template.render())

class DoLoginHandler(webapp2.RequestHandler):
    """Handle requests to login as a user of the blog site."""
    def post(self):
        """Verifies the user is registered.

        If the user is registered, then he is redirected to the main page,
        otherwise the user gets an error message indicating either the username
        does not exist, or the password is incorrect.
        """
        # Should not be the case if we got here, but check if this is a session
        # request.
        if util.is_session_req(self.request):
            self.redirect('/')
            return

        context = {
            'badname': False,
            'badpwd': False,
            'badaccount': False,
            'badpwd': False,
            'name': None
        }

        # validate username
        user = self.request.get('user')
        if not user:
            context['badname'] = True
            template = template_env.get_template('login.html')
            self.response.out.write(template.render(context))
            return

        # validate password
        pwd = self.request.get('password')
        if not pwd:
            context['badpwd'] = True
            template = template_env.get_template('login.html')
            self.response.out.write(template.render(context))
            return

        # verify account exists
        account = models.Account.get_by_id(user)
        if not account:
            context['badaccount'] = True
            context['name'] = user
            template = template_env.get_template('login.html')
            self.response.out.write(template.render(context))
            return

        # verify password is correct
        hsh = util.get_hash(account.salt, pwd)
        if hsh != account.pwd_hash:
            context['badpwd'] = True
            template = template_env.get_template('login.html')
            self.response.out.write(template.render(context))
            return

        # set session cookies
        self.response.set_cookie('name', user)
        self.response.set_cookie('secret', hsh)

        # Redirect to main page with full access
        self.redirect('/')

class RegisterHandler(webapp2.RequestHandler):
    """Handle requests to register as a user of the blog site."""
    def get(self):
        """Render the registration page."""
        # If the request is made as part of a session, then user has already signed in.
        if util.is_session_req(self.request):
            self.redirect('/')
            return

        context = {
            'badname': False,
            'nametaken': False,
            'badpwd': False,
            'name': None
        }
        template = template_env.get_template('register.html')
        self.response.out.write(template.render(context))

class DoRegisterHandler(webapp2.RequestHandler):
    """Handle requests to register as a user of the blog site."""
    def post(self):
        """Registers a user.

        Checks the username and password are valid, and the username is not
        taken. If the username is taken, then the user is prompted for another
        username. The user is redirected to the main blog page after
        registration is complete.
        """
        # If the request is made as part of a session, then user has already signed in.
        if util.is_session_req(self.request):
            self.redirect('/')
            return

        context = {
            'badname': True,
            'nametaken': False,
            'badpwd': False,
            'name': None
        }

        # Validate user name
        user = self.request.get('user')
        user = util.process_username(user)
        if not user:
            context['badname'] = True
            template = template_env.get_template('register.html')
            self.response.out.write(template.render(context))
            return

        # Check that username doesn't already exist
        account = models.Account.get_by_id(user)
        if account:
            context['nametaken'] = True
            context['name'] = user
            template = template_env.get_template('register.html')
            self.response.out.write(template.render(context))
            return

        # Validate password
        pwd = self.request.get('password')
        if not util.process_password(pwd):
            context['badpwd'] = True
            template = template_env.get_template('register.html')
            self.response.out.write(template.render(context))
            return

        # Create account
        salt = util.gensalt()
        hsh = util.get_hash(salt, pwd)
        account = models.Account(id=user, salt=salt, pwd_hash=hsh)
        try:
            account.put()
        except ndb.TransactionFailedError:
            # TODO: redirect to a page with a better error message
            s = 'Error: Unable to create account. Please try again.'
            self.response.out.write(s)
            return

        # set session cookies
        self.response.set_cookie('name', user)
        self.response.set_cookie('secret', hsh)

        # Redirect to main page with full access
        self.redirect('/')

class SaveBlogHandler(webapp2.RequestHandler):
    """Handle requests to save a blog."""
    def get(self):
        """TODO: implement logic to save a blog after it has been edited, or
        upon creation.
        """
        self.response.out.write('SaveBlogHandler not implemented yet')

# Blog comment handlers

class CreateCommentHandler(webapp2.RequestHandler):
    """Handle requests to create a comment on a blog."""
    def get(self):
        """TODO: implement"""
        self.response.out.write('CreateCommentHandler not implemented yet')

class SaveCommentHandler(webapp2.RequestHandler):
    """Handle requests to create a comment on a blog."""
    def get(self):
        """TODO: implement"""
        self.response.out.write('CreateCommentHandler not implemented yet')

class DeleteCommentHandler(webapp2.RequestHandler):
    """Handle requests to delete a comment on a blog."""
    def get(self):
        """TODO: implement"""
        self.response.out.write('DeleteCommentHandler not implemented yet')

class DeleteBlogHandler(webapp2.RequestHandler):
    """Handle requests to delete a blog."""
    def get(self):
        """TODO: implement"""
        self.response.out.write('DeleteBlogHandler not implemented yet')

class EditBlogHandler(webapp2.RequestHandler):
    """Handle requests to edit a blog."""
    def get(self):
        """TODO: implement"""
        self.response.out.write('EditBlogHandler not implemented yet')

class SignoutHandler(webapp2.RequestHandler):
    """Handle requests to signout."""
    def get(self):
        """Deletes session cookies and redirects to the main content page."""
        self.response.delete_cookie('name')
        self.response.delete_cookie('secret')
        self.redirect('/')

class CreateBlogHandler(webapp2.RequestHandler):
    """Handle requests to create a brand new blog entry."""
    def get(self):
        """Render the form to create a blog entry."""
        template = template_env.get_template('blog-form.html')
        self.response.out.write(template.render())

handlers = [
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/do-login', DoLoginHandler),
    ('/register', RegisterHandler),
    ('/do-register', DoRegisterHandler),
    ('/signout', SignoutHandler),
    ('/create-blog', CreateBlogHandler)
]
application = webapp2.WSGIApplication(handlers, debug=True)
