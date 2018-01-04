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
import re

form = """
<!DOCTYPE html>
<html>
<head>
<title>Udacity Web Dev Sign-up</title>
</head>
<body>
<h2>Sign-up</h2>
<br>
<form method="post">
    <label>
        Username
        <input type="text" name="username" value="%(username)s">
    </label>
    <span style="color: red">%(username_error)s</span>
    <br>
    <label>
        Password
        <input type="password" name="password">
    </label>
    <span style="color: red">%(pass_error)s</span>
    <br>
    <label>
        Verify Password
        <input type="password" name="verify">
    </label>
    <span style="color: red">%(verify_error)s</span>
    <br>
    <label>
        Email (optional)
        <input type="text" name="email" value="%(email)s">
    </label>
    <span style="color: red">%(email_error)s</span>
    <br>
    <input type="submit">
</form>
</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASSWORD_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    if not email:
        return True
    return EMAIL_RE.match(email)

def verify_password(str1, str2):
    return str1 == str2

class MainPage(webapp2.RequestHandler):
    def write_form(self, username_error="", pass_error="", verify_error="", email_error="", username="", email=""):
        self.response.out.write(form % {'username_error': username_error, 'pass_error': pass_error, 'verify_error': verify_error, 'email_error': email_error, 'username': username, 'email': email})

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.write_form()

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        username_error = valid_username(username)
        password_error = valid_password(password)
        email_error = valid_email(email)
        verify_error = verify_password(password, verify)

        if not username_error or not password_error or not email_error or not verify_error:
            self.write_form(username_error="Invalid username" if not username_error else "", pass_error="Invalid password" if not password_error else "",
                verify_error="Passwords don't match" if not verify_error else "", email_error="Invalid email" if not email_error else "", username=username, email=email)
        else:
            self.redirect('/welcome?username=%s' % username)

class WelcomePage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write("<h2>Welcome, %s!</h2>" % self.request.get('username'))


app = webapp2.WSGIApplication([('/', MainPage), ('/welcome', WelcomePage)], debug=True)
