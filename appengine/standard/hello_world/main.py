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

form = """
	<form action="https://google.com/search">
		<input name="q">
		<input type="submit">
	</form>
	"""

class MainPage(webapp2.RequestHandler): # It inherits from webapp2.RequestHandler
    def get(self):
        self.response.headers['Content-Type'] = 'text/html' # self.response is the global response object that the app uses. We set the Content-Type header, the default value of which is text/html
        self.response.write(form) # writes this string


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True) # URL mapping section. The "/" URL maps to the handler MainPage. MainPage defined in the class.

