__author__ = 'mmoon'
from peewee import *
from flask.ext.login import UserMixin

class User(Model, UserMixin):
    username = CharField()
    password_hash = CharField()
    first_name = CharField()
    last_name = CharField()
    email = CharField()