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

form_html = """
<form>
<h2>Add Food</h2>
<input type="text" name="food">
%s
<button>Add</button>
</form>
"""

hidden_html= """
<input type="hidden" name="food" value="%s">
"""
# hidden: include values in our query that the user can't see or interact with. This is different from type=password. Note that multiple query items can have
# the same name, so if you have a hidden input with name food and a text input with name food: ?food=val1&food=val2 is possible
shopping_html = """
<br>
<br>
<h2>Shopping List</h2>
<ul>
%s
</ul>
"""

item_html = "<li>%s</li>"

class Handler(webapp2.RequestHandler):
    def write(self, *a, **ka):
        self.response.out.write(*a, **ka)

        
class MainPage(Handler):
    def get(self):
        output = form_html
        output_hidden = ""
        output_items = ""

        items = self.request.get_all('food') # get all params with name food
        if items:

            for item in items:
                output_hidden += hidden_html % item
                output_items += item_html % item

            output_shopping = shopping_html % output_items
            output += output_shopping

        output = output % output_hidden
        self.write(output)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
