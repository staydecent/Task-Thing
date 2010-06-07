import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from lib import parseDateTime
from main import template_dir
from models.list import TaskList
from models.task import Task

class NewHandler(webapp.RequestHandler):

    def post(self, slug):
        user = users.get_current_user()
        tasklist = db.Query(TaskList).filter("slug =", slug).get()
        if not tasklist:
            self.redirect("/")
            return
        if not user:
            self.redirect("/")
            return
            
        if self.request.get('newtask'):
            task = Task(
                owner  = user,
                title  = 'New Task',
            )
            task.put()
            self.response.out.write('Saved Task.')
        
        self.redirect("/u/"+slug)


class EditHandler(webapp.RequestHandler):

    def post(self, slug):
        user = users.get_current_user()
        if not user:
            self.redirect('/')
        tasklist = db.Query(TaskList).filter("slug =", slug).get()
        key = self.request.get('key')

        if key:
            task = Task.get(key)
            
            title       = self.request.get('title')
            description = self.request.get('description')
            complete    = self.request.get('complete')
            remove      = self.request.get('remove')
            
            if title:
                task.title = title
                task.put()
                self.response.out.write(title)
                
            if description:
                task.description = description
                task.put()
                self.response.out.write(description)
            
            if complete == 'complete':
                task.complete = True
                task.put()
                self.response.out.write(complete)
            if complete == 'incomplete':
                task.complete = False
                task.put()
                self.response.out.write(complete)
                
            if remove:
                task.delete()
                self.response.out.write('Task has been removed.')
        else:
            priority = self.request.get_all('priority[]')
            if priority:
                for i,k in enumerate(priority):
                    task = Task.get(k)
                    task.priority = int(i)
                    task.put()
                self.response.out.write('Sorting saved.')
            else:
                self.response.out.write('Error')


def main():
    application = webapp.WSGIApplication([
        ("/new/([^/]+)/?", NewHandler),
        ("/edit/([^/]+)/?", EditHandler)
    ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()