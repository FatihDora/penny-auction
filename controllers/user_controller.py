#!/usr/bin/env python
# -*- coding: utf-8 -*-

import models.user

import hashlib
import random

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
	return True


def user_register(username, password):
	'''
		Register a new account
	'''
	# create a new user and hash their password
	u = user.User(username=username, create_time=now())
	u.update_password(password)
	u.put()

	# return the new user instance
	return u

def user_update_password(username, raw_password):
	# update the salt for the user
	user.password_salt = random.randint(32768, sys.maxint)

	# compute the new password hash using the new salt
	algorithm = hashlib.new("sha256")
	algorithm.update(raw_password + user.password_salt + username)
	user.hashed_password = algorithm.hexdigest()
