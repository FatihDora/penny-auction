#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# © 2013
# main author: Kevin Mershon
################################################################################

# make Python do floating-point division by default
from __future__ import division
# make string literals be Unicode strings
from __future__ import unicode_literals

import logging
from google.appengine.ext import db

class UserCookie(db.Model):
	username = db.StringProperty(required=True)
	token = db.StringProperty(required=True)
	create_time = db.DateTimeProperty(auto_now_add=True)

	@staticmethod
	def create_cookie(username,token):
		'''
			Records a cookie for the user.
		'''
		cookie = UserCookie(username=username,token=token)
		cookie.put()


	@staticmethod
	def validate_cookie(token):
		'''
			Validates a token in the cookie table.
		'''
		cookie = UserCookie.all().filter('token =',token).get()
		if cookie is None:
			return None
		else:
			return cookie

	@staticmethod
	def delete_all_cookies(username):
		db.delete(UserCookie.all().filter("username =", username)) #.filter("username =",username).fetch().delete()
