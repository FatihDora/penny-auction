#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import user, user_cookie
import lib.bcrypt.bcrypt as bcrypt
from lib import web 

from google.appengine.ext import db
from datetime import datetime
import hashlib
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

	# Verify the user exists in the database
	if not user_username_exists(username):
		raise Exception("Invalid username or password!")

	# Verify the username/password combination (including the user's password
	# salt) matches the hashed password currently stored to the user object
	hashed_password = user_hash_password(username, password, u.password_salt)
	if hashed_password != u.hashed_password:
		raise Exception("Invalid username or password")


	
	create_cookie(u.username)

	return u.username

def user_authenticate_cookie():
	'''
		This will be used to authenticate a user's cookie information.
	'''

	# TODO: We are currently using the user's username as the hash until a new
	#		hashing method is built.

	username = web.cookies().get('username')
	token = web.cookies().get('token')

	if (username == None or token == None):
		raise Exception("Invalid cookie")

	q = user_cookie.UserCookie.all().filter("username =", username).filter("token =", token)

	cookie = q.get()

	if not cookie:
		raise Exception("Invalid cookie")

	cookie.delete() # cookie was used up, so delete it
	create_cookie(username) # create new cookie

	return True

def user_register(username, email, password):
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

	if user_email_exists(email):
		raise Exception("Another account already exists with this email!")

	# create a new user and hash their password
	salt = bcrypt.gensalt()
	pass_hash = user_hash_password(username,password,salt)
	user_object = user.User(key_name=username,
							username=username,
							hashed_password=pass_hash,
							password_salt=salt,
							email=email,
							create_time=datetime.now())
	user_update_password(user_object, password)
	user_object.put()

    # return the new user instance
    return u

def user_update_password(user_object, new_password):
	'''
		Update the specified user to now have the specified salt. Also,
		recompute a random password salt
	'''
	# compute a new salt for the user
	new_salt = bcrypt.gensalt()

	# compute the new password hash using the new salt
	user_object.hashed_password = user_hash_password(user_object.username,
			new_password, new_salt)
	user_object.password_salt = new_salt
	user_object.put()

def user_hash_password(username, password, salt):
	'''
		Generate a password hash based on the provided username, password, and
		salt
	'''
	# compute the new password hash using the new salt
	return bcrypt.hashpw(password + username, salt)

def user_username_exists(username):
	'''
		Check to see if the given username exists in the database.
	'''
	user_key = db.Key.from_path("User", username)
	u = db.get(user_key)

	#Verify the user exists in the database
	if u == None:
		return False
	else:
		return True

def user_email_exists(email):
	'''
		Check to see if the given email address exists in the database.
	'''
	q = user.User.all().filter('email =', email)

	# Verify the email exists in the database
	if q.get() == None:
		return False
	else:
		return True

def create_cookie(username):
	'''
		Creates a cookie in user_cookie and sends it to the browser.
	'''

	# Cookie Design: http://jaspan.com/improved_persistent_login_cookie_best_practice
	# Cookie Syntax: http://webpy.org/cookbook/cookies

	token = bcrypt.gensalt()
	web.setcookie('username', username, 3600)
	web.setcookie('token', token, 3600)
	cookie = user_cookie.UserCookie(username=username,token=token)
	cookie.put()

	return
	
