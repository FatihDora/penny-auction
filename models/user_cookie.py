#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class UserCookie(db.Model):
	username = db.StringProperty(required=True)
	token = db.StringProperty(required=True)
	create_time = db.DateTimeProperty(auto_now_add=True)
