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
<!DOCTYPE html>
<html>
<head>
<title>Udacity Web Dev ROT13</title>
</head>
<body>
<h2>Enter some text to ROT13:</h2>
<br>
<textarea rows="4" cols="50" name="text" form="rot14">%s</textarea>
<form method="post" id="rot14">
    <input type="submit">
</form>
</body>
</html>
"""

def get_rot13(char):
    if char.isalpha():
        temp_char = ord(char) + 13
        if (char.islower() and not chr(temp_char).islower()) or (char.isupper() and not chr(temp_char).isupper()):
            temp_char += ord('a') - ord('z') - 1
        return chr(temp_char)
    return char

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(form % "")

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        rot_text =  "".join([get_rot13(char) for char in self.request.get('text')])
        self.response.out.write(form % cgi.escape(rot_text, quote = True))

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
