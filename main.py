import os

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

template_dir = os.path.join(os.path.dirname(__file__), 'views')

class MainHandler(webapp.RequestHandler):

	def get(self):
		user = users.get_current_user()
		path = os.path.join(template_dir, 'home.htm')
		if user:
			action = "<a id=\"action\" href=\"/create\">View Your Task Thing</a><p style=\"text-align:center;\"><small>You are logged in as "+user.nickname()+"</small></p>"
		else:
			action = ("<a id=\"action\" href=\"%s\">Sign In</a><p style=\"text-align:center;\"><small>Login using your Google account</small></p>" % users.create_login_url("/create"))

		self.response.out.write(template.render(path, {'action':action}))


def main():
	application = webapp.WSGIApplication([
		("/?", MainHandler)
	], debug=True)
	run_wsgi_app(application)

if __name__ == '__main__':
	main()