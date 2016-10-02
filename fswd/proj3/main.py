import datetime
import jinja2
import os
import webapp2

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
    def get(self):
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
    """Handles requests to login as a user of the blog site. """
    def get(self):
        template = template_env.get_template('login.html')
        self.response.out.write(template.render())

class RegisterPage(webapp2.RequestHandler):
    """Handles requests to register as a user of the blog site. """
    def get(self):
        template = template_env.get_template('register.html')
        self.response.out.write(template.render())

handlers = [
    ('/', MainPage),
    ('/login', LoginPage),
    ('/register', RegisterPage)
]
application = webapp2.WSGIApplication(handlers, debug=True)
