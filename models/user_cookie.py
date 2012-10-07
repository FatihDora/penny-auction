#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
		db.delete_async(UserCookie.all().filter("username=",username))
