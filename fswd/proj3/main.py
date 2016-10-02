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
        for i in range(100):
            blog_titles.append('test' + str(i))
        context = {
            'blog_titles': blog_titles,
            'loggedin': 'Login'
        }
        self.response.out.write(template.render(context))

application = webapp2.WSGIApplication([('/', MainPage)], debug=True)
