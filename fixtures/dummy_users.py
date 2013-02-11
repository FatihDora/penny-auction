#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division
# make string literals be Unicode strings
from __future__ import unicode_literals

from models import user, user_cookie
from controllers import user_controller
from google.appengine.ext import db

class DummyUsers(object):
	@staticmethod
	def setup():
		db.delete(user.User.all())
		db.delete(user_cookie.UserCookie.all())

		# admin users
		user_controller.UserController.create("Darin", "Hoover", "darin", "darinh@gmail.com", "asdf").add_bids(100)
		user_controller.UserController.create("Kevin", "Mershon", "kevin", "nwlinkvxd@gmail.com", "asdf").add_bids(100)
		user_controller.UserController.create("Brent", "Houghton", "brent", "slixbits@gmail.com", "asdf").add_bids(100)
		user_controller.UserController.create("Demo User", "Demo User", "demo user", "demo@example.com", "asdf").add_bids(100)

