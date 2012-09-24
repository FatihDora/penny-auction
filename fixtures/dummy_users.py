#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import user
from controllers import user_controller
from google.appengine.ext import db

class DummyUsers(object):
	@staticmethod
	def setup():
		db.delete(user.User.all())

		# admin users
		user_controller.user_register("darin", "darinh@gmail.com", "asdf")
		user_controller.user_register("kevin", "nwlinkvxd@gmail.com", "asdf")
		user_controller.user_register("brent", "slixbits@gmail.com", "asdf")
