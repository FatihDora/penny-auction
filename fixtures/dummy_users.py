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
		user.User.add("Darin", "Hoover", "darin", "darinh@gmail.com", "asdf").add_bids(100)
		user.User.add("Kevin", "Mershon", "kevin", "nwlinkvxd@gmail.com", "asdf").add_bids(100)
		user.User.add("Brent", "Houghton", "brent", "slixbits@gmail.com", "asdf").add_bids(100)
