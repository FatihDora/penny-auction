#!/usr/bin/env python
# -*- coding: utf-8 -*-

import models.user as user

from google.appengine.ext import db
from datetime import datetime
import hashlib
import uuid
import random
import sys

def user_get_nonce():
	'''
		Get a random number, to be used only once, hence nonce ("Number used
		ONCE")
	'''
	return random.randint(32768, sys.maxint)

def user_authenticate(username, password):
	'''
		Login to the API and return a hash which corresponds to the
		username, password, and salt
	'''
	user_key = db.Key.from_path("User", username)
	u = db.get(user_key)
	if u == None:
		raise Exception("Invalid username or password!")

	return u.hashed_password

def user_register(username, password):
	'''
		Register a new account
	'''
	# try to authenticate. if it succeeds, throw an error
	login_succeeded = False
	try:
		user_authenticate(username, password)
		login_succeeded = True
	except Exception as e:
		pass

	if login_succeeded:
		raise Exception("Another account already exists with this name!")

	# create a new user and hash their password
	u = user.User(key_name=username,
			username=username, create_time=datetime.now())
	user_update_password(u, password)
	u.put()

	# return the new user instance
	return u

def user_update_password(user_object, new_password):
	# compute a new salt for the user
	new_salt = uuid.uuid4().bytes.encode("base64").strip()
	user_object.password_salt = new_salt

	# compute the new password hash using the new salt
	algorithm = hashlib.new("sha256")
	algorithm.update(new_password + user_object.password_salt
			+ user_object.username)
	user_object.hashed_password = algorithm.hexdigest()
