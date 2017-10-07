# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import cgi

form = """
	<form method="post">
    What is your birthday?
    <br>
        <label>Month
		<input type="text" name="month" value="%(month)s">
        </label>
        <label>Day
        <input type="text" name="day" value="%(day)s">
        </label>
        <label>Year
        <input type="text" name="year" value="%(year)s">
        </label>
        <div style="color: red">%(error)s</div>
        <br>
        <br>
		<input type="submit">
	</form>
	"""
  # default method is post

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']
          
def valid_month(month):
    if month.title() in months:
        return month.title()
    return None

def valid_day(day):
    if day.isdigit() and 1 <= int(day) <= 31:
        return int(day)
    return None

def valid_year(year):
    if year.isdigit() and 1900 <= int(year) <= 2020:
        return int(year)
    return None

def escape_html(html_str):
    # Use cgi:
    return cgi.escape(html_str, quote = True)
    # Or
    """
    for (char, replacement) in (("&", "&amp;"), (">", "&gt;"), (">", "&gt;"), (">", "&gt;")): # escape html characters
        html_str = html_str.replace(char, replacement)

    return html_str"""


class MainPage(webapp2.RequestHandler): # It inherits from webapp2.RequestHandler
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {"error": escape_html(error), "month": escape_html(month), "day": escape_html(day), "year": escape_html(year)}) # see this string substitution method in python

    def get(self): # note that even though our form has method post, we never handle a post request to this URL, so we will get an error
        self.response.headers['Content-Type'] = 'text/html' # self.response is the global response object that the app uses. We set the Content-Type header, the default value of which is text/html
        self.write_form()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        print(month, day, year)

        if not month or not day or not year:
            self.write_form(error="Invalid data entered.", month=user_month, day=user_day, year=user_year) # form with old inputted values
        else:
            # self.response.out.write("Valid data received")
            # If we reload our success response in the post, we can't share a success URL and when we refresh,
            # the browser asks us "confirm resubmission...". We use a redirect to a success page/success html. Also reloading the page in this case would cause
            # our server to receive the same form with the same data and evaluate the params again for validity.
            self.redirect("/thanks") # redirecting to same domain/host, so just give a path. no need to write https:// ..

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<p>Valid data received</p><form method="post"><input type="submit" value="Submit Another Response"/></form>')

    def post(self):
        self.redirect("/")

app = webapp2.WSGIApplication([('/', MainPage), ('/thanks', ThanksHandler)], debug=True) # URL mapping section. The "/" URL maps to the handler MainPage. MainPage defined in the class.
