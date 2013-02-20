#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# © 2013
# main author: Darin Hoover, Brent Houghton, Kevin Mershon
################################################################################

# make Python do floating-point division by default
from __future__ import division
# make string literals be Unicode strings
from __future__ import unicode_literals

from fixtures import dummy_users
from fixtures import dummy_items
from fixtures import dummy_auctions

from google.appengine.ext import db
from google.appengine.ext.webapp import template
from lib import web
import os
from django.utils import simplejson as json
import logging
import datetime
from datetime import timedelta

from controllers import user_controller, auction_controller
import models.auction
import models.item as item
import models.user as user

urls = (
    '/reset_data', 'reset_data',

    '/', 'index',
    '/account','account',
    '/account/auto_bidders','account_auto_bidders',
    '/account/bidding_history','account_bidding_history',
    '/auction/(.*)','auction',
    '/bid_packs','bid_packs',
    '/checkout','checkout',
    '/support','support',
    '/winners','winners',

    '/autobidders_list_all', 'autobidders_list_all',
    '/autobidders_list_by_auction', 'autobidders_list_by_auction',
    '/autobidder_status_by_auction', 'autobidder_status_by_auction',

    '/auctions_status_by_id', 'auctions_status_by_id',
    '/auctions_list_current', 'auctions_list_current',
    '/auctions_list_all', 'auctions_list_all',
    '/auction_bid', 'auction_bid',
    '/auction_detail', 'auction_detail',
    '/auction_recent_bids', 'auction_recent_bids',
	'/auction_get_pending_bids_for_user', 'auction_get_pending_bids_for_user',
	'/auction_cancel_pending_bids_for_user', 'auction_cancel_pending_bids_for_user',
	'/auction_add_pending_bids_for_user', 'auction_add_pending_bids_for_user',

    '/persona_login', 'persona_login',
    '/user_info', 'user_info',
    '/user_username_exists', 'user_username_exists',
    '/user_email_exists', 'user_email_exists',
    '/user_logout', 'user_logout'
)

# JSON objects passed back to the client use these keys
JSON_KEY_ID = "id"
JSON_KEY_PRICE = "price"
JSON_KEY_WINNER = "winner"
JSON_KEY_REMAINING_TIME = "time_left"
JSON_KEY_IS_ACTIVE = "active"
JSON_KEY_ITEM_NAME = "name"
JSON_KEY_BASE_PRICE = "base_price"
JSON_KEY_PRODUCT_URL = "product_url"
JSON_KEY_IMAGE_URL = "image_url"


'''
    begin Webclient
'''
class index:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/index.html')
        return template.render(path, {})

class account:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/account.html')
        return template.render(path, {})

class account_bidding_history:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/bidding_history.html')
        return template.render(path, {})

class account_auto_bidders:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/auto_bidders.html')
        return template.render(path, {})

class auction:
    def GET(self, auction_id):
        path = os.path.join(os.path.dirname(__file__), 'webclient/auction.html')
        return template.render(path, {'id': auction_id})

class bid_packs:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/bid_packs.html')
        return template.render(path, {})

class checkout:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/checkout.html')
        return template.render(path, {})

class support:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/support.html')
        return template.render(path, {})

class winners:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/winners.html')
        return template.render(path, {})




'''
    end Webclient
'''


class autobidders_list_all:
    def GET(self):
        return "autobidders_list_all stub"

class autobidders_list_by_auction:
    def GET(self):
        return "autobidders_list_by_auction stub"

class autobidder_status_by_auction:
	'''
		Returns the status of a user's autobidder for a given auction
		The presence of an ID tells the client whether or not an autobidder
		exists for this auction/user combo.
	'''
	def GET(self):
		web.header('Content-Type', 'application/json')
		return json.dumps({"result":{"id":""}})

# AUCTIONS

def generate_auction_dict(auction):
	'''
		Takes an auction model object and returns the corresponding dictionary
		structure that the web client can consume; just convert to JSON and
		send back to the web client. Use this as a helper function for the many
		API methods that return auction status. Note that if the passed auction
		object is None, then None will be returned.
	'''

	if not auction:
		return None

	remaining_time = auction.auction_end - datetime.datetime.now()
	zero_time = datetime.timedelta(seconds=0)
	if remaining_time < zero_time:
		remaining_time = zero_time

	username = "No Bidders"
	if auction.current_winner:
		username = auction.current_winner.username

	return {
		JSON_KEY_ID: unicode(auction.key().id()),
		JSON_KEY_IS_ACTIVE: unicode(auction.active),
		JSON_KEY_ITEM_NAME: unicode(auction.item.name),
		JSON_KEY_BASE_PRICE: unicode(auction.item.base_price),
		JSON_KEY_PRODUCT_URL: unicode(auction.item.product_url),
		JSON_KEY_IMAGE_URL: unicode(auction.item.image_url),
		JSON_KEY_PRICE: unicode(auction.current_price),
		JSON_KEY_WINNER: unicode(username),
		JSON_KEY_REMAINING_TIME: unicode(remaining_time.total_seconds())
	}


class auctions_status_by_id:
	def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')
		auction_ids = inputs.ids

		try:
			if not auction_ids:
				raise Exception("No auction IDs were supplied in the 'ids' parameter.")

			# parse the string of IDs into a tuple of ints
			sids = auction_ids.split(',')
			if len(sids) > 40:
				raise Exception("Too many ids")

			ids = []
			for sid in sids:
				try:
					ids.append(int(sid))
				except Exception, e:
					raise Exception("The list of IDs provided could not be parsed.")
			ids = tuple(ids) 	# freeze the ID list

			try:
				auctions = auction_controller.AuctionController.auctions_status_by_ids(ids)
			except Exception, exception:
				logging.error("The following exception was raised by AuctionController.auctions_status_by_ids():\n{}".format(exception))
				#raise Exception("An internal error occurred.")

			# Build the JSON payload
			result = []

			for elem in auctions:
				result.append(generate_auction_dict(elem))

			return json.dumps({'result': result})

		except Exception, e:
			return json.dumps({'exception':unicode(e)})

class auctions_list_current:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')

        try:
			if not inputs.count:
				raise Exception("The number of auctions to list was not provided in the 'count' parameter.")

			try:
				auctions = auction_controller.AuctionController.auctions_list_current(inputs.count)

			except Exception, exception:
				logging.error("The following exception was raised by AuctionController.auctions_list_current():\n{}".format(exception))
				raise Exception("An internal error occurred.")

			# Build the JSON payload
			result = []

			for elem in auctions:
				result.append(generate_auction_dict(elem))

			return json.dumps({'result': result})

        except Exception, e:
            return json.dumps({'exception':unicode(e)})

class auctions_list_all:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')

        try:
            # TODO: check that an administrative user issued this request

			try:
				auctions = auction_controller.AuctionController.auctions_list_all()

			except Exception, exception:
				logging.error("The following exception was raised by AuctionController.auctions_list_all():\n{}".format(exception))
				raise Exception("An internal error occurred.")

			# Build the JSON payload
			result = []

			for elem in auctions:
				result.append(generate_auction_dict(elem))

			return json.dumps({'result': result})

        except Exception, e:
            return json.dumps({'exception':unicode(e)})

class auction_bid:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')

        try:

			if not inputs.id:
				raise Exception("No auction ID to bid on was given in the 'id' parameter.")

			# user validation
			username = user_controller.UserController.validate_cookie()
			if username is None:
				raise Exception("Not logged in!")

			try:
				result = auction_controller.AuctionController.auction_bid(inputs.id, username)

			except Exception, exception:
				logging.error("The following exception was raised by AuctionController.auction_bid():\n{}".format(exception))
				raise Exception("An internal error occurred.")

			return json.dumps({'result': result})

        except Exception, e:
            return json.dumps({'exception':unicode(e)})

class auction_detail:
	def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')

		try:
			if not inputs.id:
				raise Exception("No auction ID was supplied in the 'id' parameter.")

			try:
				auction = auction_controller.AuctionController.auctions_status_by_ids(int(inputs.id))
			except Exception, exception:
				logging.error("The following exception was raised by AuctionController.auctions_status_by_ids():\n{}".format(exception))
				#raise Exception("An internal error occurred.")

			result = generate_auction_dict(auction)
			return json.dumps({'result': result})

		except Exception, e:
			return json.dumps({'exception':unicode(e)})

class auction_recent_bids:
    def GET(self):

		inputs = web.input()
		web.header('Content-Type', 'application/json')
		try:

			result = []
			result.append({username:'kevin',price:'1.20',bidtime:'05:14:23 PM'})
			result.append({username:'darin',price:'1.19',bidtime:'05:14:15 PM'})
			result.append({username:'brent',price:'1.18',bidtime:'05:14:10 PM'})
			result.append({username:'kevin',price:'1.17',bidtime:'05:14:09 PM'})
			result.append({username:'chris',price:'1.16',bidtime:'05:14:02 PM'})
			result.append({username:'kevin',price:'1.15',bidtime:'05:13:58 PM'})
			result.append({username:'darin',price:'1.14',bidtime:'05:13:49 PM'})
			result.append({username:'brent',price:'1.13',bidtime:'05:13:42 PM'})
			result.append({username:'chris',price:'1.12',bidtime:'05:13:36 PM'})

			return json.dumps({'result':result})

		except Exception, e:
			return json.dumps({'exception':unicode(e)})



class auction_add_pending_bids_for_user:
    def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')

		try:
			if not inputs.id:
				raise Exception("No auction ID was supplied in the 'id' parameter.")

			if not inputs.num_bids:
				raise Exception("No number of bids was supplied in the 'num_bids' parameter.")

			# user validation
			user_name = user_controller.UserController.validate_cookie()
			if user_name is None:
				raise Exception("Not logged in!")

			try:
				result = auction_controller.AuctionController.attach_autobidder(
						auction_id=int(inputs.id),
						user_name=user_name,
						num_bids=inputs.num_bids
				)

			except Exception, exception:
				logging.error("The following exception was raised by AuctionController.attach_autobidder():\n{}".format(exception))
				raise Exception("An internal error occurred.")

			return json.dumps({'result': result})

		except Exception, e:
			return json.dumps({'exception':unicode(e)})

class auction_get_pending_bids_for_user:
    def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')

		try:
			if not inputs.id:
				raise Exception("No auction ID was supplied in the 'id' parameter.")

			# user validation
			user_name = user_controller.UserController.validate_cookie()
			if user_name is None:
				raise Exception("Not logged in!")

			try:
				result = auction_controller.AuctionController.get_autobidder_remaining_bids(
						auction_id=int(inputs.auction_id),
						user_name=user_name
				)

			except Exception, exception:
				logging.error("The following exception was raised by AuctionController.get_autobidder_remaining_bids():\n{}".format(exception))
				raise Exception("An internal error occurred.")

			return json.dumps({'result': result})

		except Exception, e:
			return json.dumps({'exception':unicode(e)})

class auction_cancel_pending_bids_for_user:
    def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')

		return json.dumps({'result': unicode(result)})

		try:
			if not inputs.id:
				raise Exception("No auction ID was supplied in the 'id' parameter.")

			# user validation
			user_name = user_controller.UserController.validate_cookie()
			if user_name is None:
				raise Exception("Not logged in!")

			try:
				result = auction_controller.AuctionController.cancel_autobidder(
						auction_id=int(inputs.id),
						user_name=user_name
				)

			except Exception, exception:
				logging.error("The following exception was raised by AuctionController.cancel_autobidder():\n{}".format(exception))
				raise Exception("An internal error occurred.")

			return json.dumps({'result': result})

		except Exception, e:
			return json.dumps({'exception':unicode(e)})


# USER Stuff

class user_info:
	def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')

		try:
			result = {'result':user_controller.UserController.user_info()}
			return json.dumps(result)
		except Exception, exception:
			logging.exception(exception)
			return json.dumps({'result': False, 'error': 'An internal server error caused the login process to fail.'})

class user_logout:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')

        try:
            result = {'result':user_controller.UserController.user_logout()}
            return json.dumps(result)

        except Exception, e:
            return json.dumps({'exception':unicode(e)})

class persona_login:
	def GET(self):
		inputs = web.input(assertion=None)
		web.header('Content-Type', 'application/json')
		try:
			this_user = user_controller.UserController.persona_login(inputs.assertion)
			if this_user:
				result = {'result': True, 'username': this_user.username}
			else:
				result = {'result': False, 'username': None}
		except Exception, exception:
			logging.exception(exception)
			return json.dumps({'result': False, 'error': 'An internal server error caused the login process to fail.'})

		return json.dumps(result)

class user_authenticate_cookie:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')
        try:
            result ={'result':user_controller.UserController.user_authenticate_cookie()}
            return json.dumps(result)

        except Exception, e:
            return json.dumps({'exception':unicode(e)})


class user_username_exists:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')

        try:
			if not inputs.username:
				raise Exception('required string parameter "username" was not passed to the server, or was an empty string')

			result = user_controller.UserController.user_username_exists(inputs.username)
			return json.dumps({'result': result})
        except Exception, e:
            return json.dumps({'exception':unicode(e)})

class user_email_exists:
    def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')

		try:
			if not inputs.email:
				raise Exception('required string parameter "email" was not passed to the server, or was an empty string')

			result = user_controller.UserController.user_email_exists(inputs.email)
			return json.dumps({'result': result})
		except Exception, e:
			return json.dumps({'exception':unicode(e)})

class reset_data:
    def GET(self):
		br = '<br/>'
		result = ""
		result += 'Loading Data...' + br
		dummy_users.DummyUsers.setup()
		dummy_items.DummyItems.setup()
		dummy_auctions.DummyAuctions.setup()
		result += 'Done...' + br

		return result


app = web.application(urls, globals())
application = app.gaerun()
if (os.getenv("APPLICATION_ID").startswith("dev~")):
    logging.getLogger().setLevel(logging.ERROR)

