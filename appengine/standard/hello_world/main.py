import webapp2
import cgi
import jinja2
import os

# type hidden: include values in our query that the user can't see or interact with. This is different from type=password. Note that multiple query items can have
# the same name, so if you have a hidden input with name food and a text input with name food: ?food=val1&food=val2 is possible

template_dir = os.path.join(os.path.dirname(__file__), 'templates') # os.path.dirname(__file__) is location of this file
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True) # when we render templates, jinja will look for them in this directory

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template) # create a jinja template from the file argument template
        return t.render(params) # see example

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw)) # send to browser

        
class MainPage(Handler):
    def get(self):
        items = self.request.get_all('food') # get all params with name food
        self.render("shopping_list.html", items=items) # again, we are dealing with user input. Consider data validation and HTML escaping

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
