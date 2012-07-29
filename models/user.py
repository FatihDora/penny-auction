#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class User(db.Model):
	id = db.IntegerProperty()
	username = db.StringProperty()
	hashed_password = db.StringProperty()
	password_salt = db.StringProperty()
	create_time = db.DateTimeProperty()
	personal_information = db.StringProperty()
