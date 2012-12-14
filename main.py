#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
import models.bid_history as bid_history
import models.item as item
import models.user as user

urls = (
    '/reset_data', 'reset_data',

    '/', 'index',
    '/account','account',
    '/account/auto_bidders','account_auto_bidders',
    '/account/bidding_history','account_bidding_history',
    '/auction/.*','auction',
    '/bid_packs','bid_packs',
    '/checkout','checkout',
    '/forgot_credentials','forgot_credentials',
    '/register','register',
    '/support','support',
    '/validate_email','validate_email',
    '/winners','winners',
    
    '/autobidders_list_all', 'autobidders_list_all',
    '/autobidders_list_by_auction', 'autobidders_list_by_auction',

    '/auctions_status_by_id', 'auctions_status_by_id',
    '/auctions_list_current', 'auctions_list_current',
    '/auctions_list_all', 'auctions_list_all',
    '/auction_bid', 'auction_bid',
    '/auction_detail', 'auction_detail',
    '/auction_recent_bids', 'auction_recent_bids',
	'/auction_add_pending_bids', 'auction_add_pending_bids',
	'/auction_get_pending_bids_for_user', 'auction_get_pending_bids_for_user',
	'/auction_cancel_pending_bids_for_user', 'auction_cancel_pending_bids_for_user',
	'/auction_add_pending_bids_for_user', 'auction_add_pending_bids_for_user',
	'/auction_remove_pending_bids_for_user', 'auction_remove_pending_bids_for_user',

    '/user_get_nonce', 'user_get_nonce',
    '/user_register', 'user_register',
    '/user_validate_email', 'user_validate_email',
    '/user_authenticate', 'user_authenticate',
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
    def GET(self):
        auction_id = web.ctx.path.replace("/auction/","")
        path = os.path.join(os.path.dirname(__file__), 'webclient/auction.html')
        return template.render(path, {'id':auction_id})

class bid_packs:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/bid_packs.html')
        return template.render(path, {})

class checkout:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/checkout.html')
        return template.render(path, {})

class forgot_credentials:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/forgot_credentials.html')
        return template.render(path, {})

class register:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/register.html')
        return template.render(path, {})

class support:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/support.html')
        return template.render(path, {})

class validate_email:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/validate_email.html')
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
	zero_time = datetime.datetime.timeremaining_time(seconds=0)
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

        try:
			if not auction_ids:
				raise Exception("No auction IDs were supplied in the 'auction_ids' parameter.")

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
				raise Exception("An internal error occurred.")

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
				auction = auction_controller.AuctionController.auctions_status_by_ids((inputs.id))

			except Exception, exception:
				logging.error("The following exception was raised by AuctionController.auctions_status_by_ids():\n{}".format(exception))
				raise Exception("An internal error occurred.")

			result = generate_auction_dict(auction)
			return json.dumps({'result': result})

        except Exception, e:
            return json.dumps({'exception':unicode(e)})

class auction_recent_bids:
    def GET(self):
        inputs = web.inputs
        web.header('Content-Type', 'application/json')

		# stub
        ad = []
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:58'})
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:52'})
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:47'})
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:44'})
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:40'})
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:33'})
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:32'})
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:29'})
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:24'})
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:21'})
        return json.dumps({'result':ad}) 

class auction_add_pending_bids:
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

class auction_add_pending_bids_for_user:
    def GET(self):
		# stub
        return "auction_add_pending_bids_for_user stub"

class auction_remove_pending_bids_for_user:
    def GET(self):
		# stub
        return "auction_remove_pending_bids_for_user stub"

# USER Stuff

class user_info:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')

        try:
            result = {'result':user_controller.UserController.user_info()}
            return json.dumps(result)

        except Exception, e:
            return json.dumps({'exception':unicode(e)})

class user_logout:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')

        try:
            result = {'result':user_controller.UserController.user_logout()}
            return json.dumps(result)

        except Exception, e:
            return json.dumps({'exception':unicode(e)})


class user_register:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')
        try:
            result = {'result':user_controller.UserController.user_register(inputs.first_name,inputs.last_name,inputs.username,inputs.email,inputs.password)}
            return json.dumps(result)

        except Exception, e:
            return json.dumps({'exception':unicode(e)})

class user_validate_email:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')
        try:
            result = {'result':user_controller.UserController.user_validate_email(inputs.code)}
            return json.dumps(result)

        except Exception, e:
            return json.dumps({'exception':unicode(e)})

class user_authenticate:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')
        try:
            result ={'result':user_controller.UserController.user_authenticate(inputs.username, inputs.password)}
            return json.dumps(result)

        except Exception, e:
            return json.dumps({'exception':unicode(e)})

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

