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
		user_controller.UserController.create(first_name="Darin", last_name="Hoover", username="darin", email="darinh@gmail.com").add_bids(100)
		user_controller.UserController.create(first_name="Kevin", last_name="Mershon", username="kevin", email="nwlinkvxd@gmail.com").add_bids(100)
		user_controller.UserController.create(first_name="Brent", last_name="Houghton", username="brent", email="slixbits@gmail.com").add_bids(100)

