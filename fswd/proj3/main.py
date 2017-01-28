import datetime
import jinja2
import os
import webapp2
import util
import models
import hmac
import json
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
            return self.redirect('/')
        template = template_env.get_template('signin.html')
        return self.response.out.write(template.render(self.get_context()))

    def get_context(self):
        '''Create the context for the login page.'''
        return {
            'action': 'sign in',
            'primary_action': 'do-login',
            'secondary_action': 'register',
            'message': "Don't have an account yet? Register..."
        }

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
            return self.redirect('/')

        data = json.loads(self.request.body)
        data['success'] = False
        user = data['user']
        pwd = data['password']

        # verify account exists
        account = models.Account.get_by_id(user)
        if not account:
            data['baduser'] = True
            return self.response.out.write(json.dumps(data))

        # verify password is correct
        hsh = util.get_hash(account.salt, pwd)
        if hsh != account.pwd_hash:
            data['badpwd'] = True
            return self.response.out.write(json.dumps(data))

        # set session cookies
        data['success'] = True
        self.response.set_cookie('name', user)
        self.response.set_cookie('secret', hsh)
        return self.response.out.write(json.dumps(data))

class RegisterHandler(webapp2.RequestHandler):
    """Handle requests to register as a user of the blog site."""
    def get(self):
        """Render the registration page."""
        # If the request is made as part of a session, then user has already signed in.
        if util.is_session_req(self.request):
            return self.redirect('/')
        template = template_env.get_template('signin.html')
        self.response.out.write(template.render(self.get_context()))

    def get_context(self):
        """Return the context for the register.html template."""
        return {
            'action': 'register',
            'primary_action': 'do-register',
            'secondary_action': 'login',
            'message': "Have an account already? Sign in..."
        }

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

        data = json.loads(self.request.body)
        user = data['user']
        pwd = data['password']

        # Check that username doesn't already exist
        account = models.Account.get_by_id(user)
        if account:
            data['success'] = False
            return self.response.out.write(json.dumps(data))

        # Validate password
        if not util.process_password(pwd):
            data['success'] = False
            return self.response.out.write(json.dumps(data))

        # Create account
        salt = util.gensalt()
        hsh = util.get_hash(salt, pwd)
        account = models.Account(id=user, salt=salt, pwd_hash=hsh)
        try:
            account.put()
        except ndb.TransactionFailedError:
            data['success'] = False
            return self.response.out.write(json.dumps(data))

        data['success'] = True
        self.response.set_cookie('name', user)
        self.response.set_cookie('secret', hsh)
        return self.response.out.write(json.dumps(data))

# Blog comment handlers

class CreateCommentHandler(webapp2.RequestHandler):
    """Handle requests to create a comment on a blog."""
    def post(self, urlkey):
        """Stores a comment in the datastore and redirects user to main page."""
        name = self.request.cookies.get('name')
        text = self.request.get('text')
        blogkey = ndb.Key(urlsafe=urlkey)
        comment = models.BlogComment(blog=blogkey, user=name, comment=text)
        try:
            comment.put()
        except ndb.TransactionFailedError:
            # TODO: Handle error
            pass
        return self.redirect('/blog/%s' % urlkey)

class SignoutHandler(webapp2.RequestHandler):
    """Handle requests to signout."""
    def get(self):
        """Deletes session cookies and redirects to the main content page."""
        self.response.delete_cookie('name')
        self.response.delete_cookie('secret')
        return self.redirect('/')

class CreateBlogHandler(webapp2.RequestHandler):
    """Handle requests to create a brand new blog entry."""
    def post(self):
        """Handles a post request to create a blog entry."""
        # TODO: verify request is made in session context
        action = self.request.get('action')
        if action == 'create':
            self.create()
        return self.redirect('/')

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
    """Handles request initial request to create a blog entry."""
    def get(self):
        """Render the form to create a blog entry."""
        template = template_env.get_template('blog-form.html')
        return self.response.out.write(template.render(self.get_context()))

    def get_context(self):
        """Creates the context for the template."""
        context = {
            'action': 'create-blog',
            'with_title': True,
            'label_title': 'Blog'
        }
        return context

class EditBlogHandler(webapp2.RequestHandler):
    """Handles a request to edit a blog entry."""
    def get(self, urlkey):
        """Renders the form to edit a blog entry."""
        blog = ndb.Key(urlsafe=urlkey).get()
        context = self.get_context(blog)
        template = template_env.get_template('blog-form.html')
        return self.response.out.write(template.render(context))

    def get_context(self, blog):
        """Create the context for the edit form template."""
        return {
            'action': 'save-blog',
            'with_title': True,
            'entry_id': blog.key.urlsafe(),
            'label_title': 'Blog',
            'title_value': blog.title,
            'text_value': blog.text
        }

class SaveBlogHandler(webapp2.RequestHandler):
    """Handles a request to save a blog after an edit."""
    def post(self, urlkey):
        """Saves, deletes, or cancels editing a blog entry.

        Args:
            urlkey: Blog key in url safe format.
        """
        action = self.request.get('action')
        if action == 'cancel':
            return self.redirect('/blog/%s' % urlkey)
        elif action == 'delete':
            ndb.Key(urlsafe=urlkey).delete()
            return self.redirect('/')
        elif action == 'save':
            self.save_blog(urlkey)
            return self.redirect('/blog/%s' % urlkey)
        # should never get here, but just in case
        return self.redirect('/blog/%s' % urlkey)

    def save_blog(self, urlkey):
        """Save the contents of the edited blog.

        Args:
            urlkey: Blog key in url safe format.
        """
        blog = ndb.Key(urlsafe=urlkey).get()
        blog.title = self.request.get('title').strip()
        blog.text = self.request.get('text').strip()
        # TODO: might be a good idea to add a last edited field to blog model
        try:
            blog.put()
        except ndb.TransactionFailedError:
            # TODO: handle error
            pass

class ViewBlogHandler(webapp2.RequestHandler):
    """Handlers requests to view a blog entry."""
    def get(self, urlkey):
        """Renders a blog entry.

        Args:
            urlkey: The blog key in URL-friendly form.
        """
        blog = ndb.Key(urlsafe=urlkey).get()
        login_status = util.is_session_req(self.request)
        q = models.BlogComment.query(models.BlogComment.blog == blog.key)
        comments = q.order(models.BlogComment.date).fetch()
        context = self.get_context(blog, login_status, comments)
        # check if user likes blog
        if login_status:
            name = self.request.cookies.get('name')
            context['user'] = name
            account = models.Account.get_by_id(name)
            if account.key in blog.likes:
                context['like_status'] = True
                context['heart'] = 'red-heart'
        template = template_env.get_template('blog.html')
        return self.response.out.write(template.render(context))

    def get_context(self, blog, login_status, comments, user=None):
        """Creates the dictionary context for the template.

        Args:
            blog: The blog entry model.
            login_status: Login status of user making request.
            comments: List of blog comments.
        """
        return {
            'blog': blog ,
            'loggedin': login_status,
            'blog_id': blog.key.urlsafe(),
            'comments': comments,
            'like_status': False,
            'heart': 'normal',
            'user': user
        }

class EditCommentHandler(webapp2.RequestHandler):
    """Responds to a request to edit a comment in a blog."""
    def get(self, urlkey):
        """Renders the form to edit a comment entry."""
        comment = ndb.Key(urlsafe=urlkey).get()
        template = template_env.get_template('blog-form.html')
        context = self.get_context(comment)
        return self.response.out.write(template.render(context))

    def get_context(self, comment):
        """Create the context for the comment form template."""
        return {
            'action': 'save-comment',
            'with_title': False,
            'entry_id': comment.key.urlsafe(),
            'label_title': 'Comment',
            'text_value': comment.comment
        }

class SaveCommentHandler(webapp2.RequestHandler):
    """Responds to a request to save a blog comment after it has been edited."""
    def post(self, urlkey):
        """Saves or deletes the comment and redirects to blog post."""
        comment = ndb.Key(urlsafe=urlkey).get()
        action = self.request.get('action')
        if action == 'cancel':
            return self.redirect('/blog/'+comment.blog.urlsafe())
        if action == 'delete':
            return self.redirect('/delete-comment/'+urlkey)
        text = self.request.get('text').strip()
        # Delete if comment is empty
        if not len(text):
            return self.redirect('/delete-comment/'+urlkey)
        # Don't commit if comment hasn't changed
        if comment.comment == text:
            return self.redirect('/blog/'+comment.blog.urlsafe())
        comment.comment = text;
        try:
            comment.put()
        except ndb.TransactionFailedError:
            # TODO: handle error
            pass
        return self.redirect('/blog/'+comment.blog.urlsafe())

class DeleteCommentHandler(webapp2.RequestHandler):
    """Responds to a request to delete a comment in a blog."""
    def get(self, urlkey):
        """Deletes a comment from the DB and redirects to blog post.

            Args:
                urlkey: A url-safe version of the comment DB key.
        """
        comment = ndb.Key(urlsafe=urlkey).get()
        try:
            comment.key.delete()
        except ndb.TransactionFailedError:
            # TODO: handle error
            pass
        return self.redirect('/blog/'+comment.blog.urlsafe())

class LikeBlogHandler(webapp2.RequestHandler):
    """Responds to a request to like a blog entry."""
    def get(self, urlkey):
        """Adds like if user is logged in."""
        # Should not get here if user is not logged in, but check either way
        if not util.is_session_req(self.request):
            return self.redirect('/login')
        name = self.request.cookies.get('name')
        account = models.Account.get_by_id(name)
        blog = ndb.Key(urlsafe=urlkey).get()
        data = {'add': False, 'remove': False}
        # Don't allow users to like their own blogs
        if blog.is_author(name):
            return self.response.out.write(json.dumps(data))

        # User is unliking
        if account.key in blog.likes:
            blog.likes.remove(account.key)
            try:
                blog.put()
                data['remove'] = True
            except ndb.TransactionFailedError:
                # TODO: handle error as internal server error
                pass
            return self.response.out.write(json.dumps(data))

        # User is liking
        blog.likes.append(account.key)
        try:
            blog.put()
            data['add'] = True
        except ndb.TransactionFailedError:
            # TODO: handle error as internal server error
            pass
        return self.response.out.write(json.dumps(data))

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
    (r'/create-comment/(\S+)', CreateCommentHandler),
    (r'/edit-comment/(\S+)', EditCommentHandler),
    (r'/save-comment/(\S+)', SaveCommentHandler),
    (r'/delete-comment/(\S+)', DeleteCommentHandler),
    (r'/like/(\S+)', LikeBlogHandler),
    (r'/edit-blog/(\S+)', EditBlogHandler),
    (r'/save-blog/(\S+)', SaveBlogHandler)
]
application = webapp2.WSGIApplication(handlers, debug=True)
