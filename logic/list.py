import os

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from main import template_dir
from lib import parseDateTime
from models.list import TaskList
from models.task import Task

class CreateHandler(webapp.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect('/')
        else:
            existing = db.Query(TaskList).filter("owner =", user).get()
            if not existing:
                tasklist = TaskList(
                    owner = user,
                    slug  = user.user_id()
                )
                tasklist.put()
            
            self.redirect("/u/" + user.user_id())


class ListHandler(webapp.RequestHandler):
    
    def get(self, slug):
        user = users.get_current_user()
        if not user:
            self.redirect('/')
        if slug != user.user_id():
            self.redirect('/')
        tasklist = db.Query(TaskList).filter("slug =", user.user_id()).get()
        if not tasklist:
            self.redirect("/")
            return
        
        data = {
            'list'      :tasklist,
            'user'      :user
        }
        path = os.path.join(template_dir, 'list.htm')
        self.response.out.write(template.render(path, data))
        
        
class TaskHandler(webapp.RequestHandler):
    
    def get(self, slug):
        tasklist = db.Query(TaskList).filter("slug =", slug).get()
        if not tasklist:
            self.redirect("/")
            return
            
        data = {
            'tasks'     :db.Query(Task).filter("owner =", tasklist.owner).order('priority').fetch(limit=20)
        }
        path = os.path.join(template_dir, 'tasks.htm')
        self.response.out.write(template.render(path, data))
        

def main():
    application = webapp.WSGIApplication([
        ("/create/?", CreateHandler),
        ("/u/([^/]+)/?", ListHandler),
        ("/tasks/([^/]+)/?", TaskHandler)
    ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()