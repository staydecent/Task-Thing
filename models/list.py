import os

from google.appengine.ext import db

class TaskList(db.Model):
    owner       = db.UserProperty()
    slug		= db.StringProperty()
    styles		= db.TextProperty(required=False)
    created_at  = db.DateTimeProperty(auto_now_add=True)