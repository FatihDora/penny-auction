#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division

from google.appengine.ext import db
from lib import web

from controllers import user_controller

urls = (
	'/', 'index',
	'/create_auto_bidder', 'create_auto_bidder',
	'/get_auto_bidder_status', 'get_auto_bidder_status',
	'/cancel_auto_bidder', 'cancel_auto_bidder',
	'/list_auto_bidders_for_user', 'list_auto_bidders_for_user',
	'/list_auto_bidders_for_auction', 'list_auto_bidders_for_auction',

	'/get_nonce', 'get_nonce',
	'/user_register', 'register',
	'/user_authenticate', 'authenticate',
	'/user_username_exists', 'username_exists',
	'/user_email_exists', 'email_exists'
)


class index:
	def GET(self):
		return "index stub"

class create_auto_bidder:
	def GET(self):
		return "create_auto_bidder stub"

class cancel_auto_bidder:
	def GET(self):
		return "cancel_auto_bidder stub"

class list_auto_bidders:
	def GET(self):
		return "list_auto_bidder stub"

class get_auto_bidder_status:
	def GET(self):
		return "get_auto_bidder_status stub"

class list_auto_bidders_for_auction:
	def GET(self):
		return "list_auto_bidders_for_auction stub"



class get_nonce:
	def GET(self):
		return user_controller.user_get_nonce()

class register:
	def GET(self):
		inputs = web.input()
		try:
			return user_controller.user_register(inputs.username, inputs.email, inputs.password).username
		except Exception as e:
			return e

class authenticate:
	def GET(self):
		inputs = web.input()
		try:
			return user_controller.user_authenticate(inputs.username, inputs.password)
		except Exception as e:
			return e

class username_exists:
	def GET(self):
		inputs = web.input()
		try:
			return user_controller.user_username_exists(inputs.username)
		except Exception as e:
			return e
	
class email_exists:
	def GET(self):
		inputs = web.input()
		try:
			return user_controller.user_email_exists(inputs.email)
		except Exception as e:
			return e
		
app = web.application(urls, globals())
main = app.cgirun()

