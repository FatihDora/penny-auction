#!/usr/bin/env python

from google.appengine.ext import db
import web


urls = (
	'/create_auto_bidder', 'create_auto_bidder',
	'/get_auto_bidder_status', 'get_auto_bidder_status',
	'/cancel_auto_bidder', 'cancel_auto_bidder',
	'/list_auto_bidders_for_user', 'list_auto_bidders_for_user',
	'/list_auto_bidders_for_auction', 'list_auto_bidders_for_auction'
)


class create_auto_bidder:
	def GET(self):
		return "<something>"

class cancel_auto_bidder:
	def GET(self):
		return "<something>"

class list_auto_bidders:
	def GET(self):
		return "<something>"

class get_auto_bidder_status:
	def GET(self):
		return "<something>"

class list_auto_bidders_for_auction:
	def GET(self):
		return "<something>"


app = web.application(urls, globals())
main = app.cgirun()

