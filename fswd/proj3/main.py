import datetime
import jinja2
import os
import webapp2

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
