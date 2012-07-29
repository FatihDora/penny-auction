#!/usr/bin/env python

from google.appengine.ext import db
from lib import web


urls = (
	'/', 'index',
	'/create_auto_bidder', 'create_auto_bidder',
	'/get_auto_bidder_status', 'get_auto_bidder_status',
	'/cancel_auto_bidder', 'cancel_auto_bidder',
	'/list_auto_bidders_for_user', 'list_auto_bidders_for_user',
	'/list_auto_bidders_for_auction', 'list_auto_bidders_for_auction'
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
		return user.get_nonce()

class login:
	def GET(self):
		return user.login()

class logout:
	def GET(self):
		return user.logout()

class validate_email:
	def GET(self):
		return user.validate_email()


app = web.application(urls, globals())
main = app.cgirun()

