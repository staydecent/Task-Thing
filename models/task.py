import os

from google.appengine.ext import db

class Task(db.Model):
    owner       = db.UserProperty()
    title       = db.StringProperty()
    complete    = db.BooleanProperty(default=False)
    description = db.TextProperty(required=False)
    priority    = db.IntegerProperty(required=False)
    updated_at  = db.DateTimeProperty(auto_now=True)
    created_at  = db.DateTimeProperty(auto_now_add=True)