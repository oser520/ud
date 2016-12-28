import datetime
import jinja2
import os
import webapp2
import util
import models
import hmac
from google.appengine.ext import ndb

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

class MainHandler(webapp2.RequestHandler):
    """Handle requests to the main blog site."""
    def get(self):
        # Get session status
        logged_status = util.is_session_req(self.request)
        template = template_env.get_template('content.html')
        context = {
            'blog_titles': models.Blog.query().order(-models.Blog.date).fetch(),
            'loggedin': logged_status
        }
        self.response.headers.add('Cache-Control', 'no-store')
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
            return self.redirect('/')

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
            return self.response.out.write(template.render(context))

        # Check that username doesn't already exist
        account = models.Account.get_by_id(user)
        if account:
            context['nametaken'] = True
            context['name'] = user
            template = template_env.get_template('register.html')
            return self.response.out.write(template.render(context))

        # Validate password
        pwd = self.request.get('password')
        if not util.process_password(pwd):
            context['badpwd'] = True
            template = template_env.get_template('register.html')
            return self.response.out.write(template.render(context))

        # Create account
        salt = util.gensalt()
        hsh = util.get_hash(salt, pwd)
        account = models.Account(id=user, salt=salt, pwd_hash=hsh)
        try:
            account.put()
        except ndb.TransactionFailedError:
            # TODO: redirect to a page with a better error message
            s = 'Error: Unable to create account. Please try again.'
            return self.response.out.write(s)

        # set session cookies
        self.response.set_cookie('name', user)
        self.response.set_cookie('secret', hsh)

        # Redirect to main page with full access
        return self.redirect('/')

# Blog comment handlers

class CreateCommentHandler(webapp2.RequestHandler):
    """Handle requests to create a comment on a blog."""
    def post(self, urlkey):
        """Stores a comment in the datastore and redirects user to main page."""
        action = self.request.get('action')
        if action == 'create':
            self.create(urlkey)
        """TODO: redirect to comment"""
        self.redirect('/')

    def create(self, urlkey):
        """Stores a blog comment in the datastore."""
        name = self.request.cookies.get('name')
        title = self.request.get('title')
        text = self.request.get('text')
        blogkey = ndb.Key(urlsafe=urlkey)
        comment = models.BlogComment(blog=blogkey, user=name, comment=text)
        try:
            comment.put()
        except ndb.TransactionFailedError:
            # TODO: Handle error
            return

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
    def post(self):
        """Handles a post request to create a blog entry."""
        # TODO: verify request is made in session context
        action = self.request.get('action')
        if action == 'create':
            self.create()
        self.redirect('/')
    def create(self):
        """Creates a blog entry."""
        name = self.request.cookies.get('name')
        title = self.request.get('title')
        text = self.request.get('text')
        blog = models.Blog(user=name, title=title, text=text)
        try:
            blog.put()
        except ndb.TransactionFailedError:
            # TODO: Handle error
            return

class BlogFormHandler(webapp2.RequestHandler):
    """Renders the blog form to create a blog entry."""
    def get(self):
        """Render the form to create a blog entry."""
        context = {
            'entry_type': 'blog',
            'with_title': True
        }
        template = template_env.get_template('blog-form.html')
        self.response.out.write(template.render(context))

class ViewBlogHandler(webapp2.RequestHandler):
    """Handlers requests to view a blog entry."""
    def get(self, urlkey):
        """Renders a blog entry.

        Args:
            urlkey: The blog key in URL representation.
        """
        key = ndb.Key(urlsafe=urlkey)
        blog = key.get()
        template = template_env.get_template('blog.html')
        logged_status = util.is_session_req(self.request)
        q = models.BlogComment.query(models.BlogComment.blog == key)
        comments = q.order(models.BlogComment.date).fetch()
        context = {
            'blog': blog ,
            'loggedin': logged_status,
            'blog_id': urlkey,
            'comments': comments
        }
        self.response.out.write(template.render(context))

class CommentFormHandler(webapp2.RequestHandler):
    """Responds to a request to create a comment in a blog."""
    def get(self, urlkey):
        """Render the form to create a comment entry."""
        context = {
            'entry_type': 'comment',
            'with_title': False,
            'blog_id': urlkey
        }
        template = template_env.get_template('blog-form.html')
        self.response.out.write(template.render(context))

handlers = [
    (r'/', MainHandler),
    (r'/login', LoginHandler),
    (r'/do-login', DoLoginHandler),
    (r'/register', RegisterHandler),
    (r'/do-register', DoRegisterHandler),
    (r'/signout', SignoutHandler),
    (r'/create-blog', CreateBlogHandler),
    (r'/blog-form', BlogFormHandler),
    (r'/blog/(\S+)', ViewBlogHandler),
    (r'/comment-form/(\S+)', CommentFormHandler),
    (r'/create-comment/(\S+)', CreateCommentHandler)
]
application = webapp2.WSGIApplication(handlers, debug=True)
