#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import auction, item, user
from controllers import user_controller
from datetime import timedelta
import datetime
import logging

from google.appengine.ext import db

def invoke_auto_bidders(auction):
	''' Pass an Auction object to have the next auto bidder attached to that
	auction place a bid. If no auto bidders with remaining bids are
	attached, nothing happens. '''

	next_auto_bidder = None
	for this_auto_bidder in auction.attached_autobidders:
		if next_auto_bidder is None or this_auto_bidder.last_bid_time < next_auto_bidder.last_bid_time:
			next_auto_bidder = this_auto_bidder

	# shortcut out if there are no autobidders on this auction
	if next_auto_bidder is None:
		return
	
	next_auto_bidder.use_bid()
	auction.place_bid(next_auto_bidder.owner)

def auctions_status_by_id(auction_ids):
	'''
		List the auctions specified
	'''
	if not auction_ids:
		return

	# Try to parse the IDs and create a list of ints.
	try:
		sids = auction_ids.split(',')
	except Exception, e:
		raise Exception("The list of IDs provided could not be parsed.")
	ids = []
	for sid in sids:
		try:
			ids.append(int(sid))
		except Exception, e:
			raise Exception("The list of IDs provided could not be parsed.")

	if len(ids) > 40:
		raise Exception("Too many ids")

	# Try to get some auctions from the list of IDs
	auctions = auction.Auction.get_by_id(ids)

	if not auctions:
		raise Exception("No auctions returned.")

	# Build the JSON payload
	result = []
	delta = ""

	for elem in auctions:
		try:
			if not elem:
				continue

			delta = elem.auction_end - datetime.datetime.now()
			if delta.total_seconds() <= 0:
				delta = timedelta(seconds=0)
				elem.active = False
				elem.put()
				# Do winner stuff here... apparently our daemon hasn't gotten to this one.

			username = "No Bidders"
			if elem.current_winner:
				username = elem.current_winner.username

			price = "0.00"
			if elem.current_price:
				price = "{0:.2f}".format(elem.current_price)
			# i: ID
			# p: currentPrice
			# w: currentWinner
			# t: timeTilEnd
			# a: active

			result.append({'i':str(elem.key().id()),'p':str(price),'w':str(username),'t':str(delta.total_seconds()),'a':str(elem.active)})
		except Exception, e:
			print e

	if result is None:
		raise Exception("There were no auctions for the IDs you provided.")


	return result
	

def auctions_list_active(count=10):
	'''
		List the currently-running auctions
	'''
	auctions = auction.Auction.get_active(count)

	if not auctions:
		raise Exception("No active auctions.")

	# Build the JSON payload
	result = []
	delta = ""

	for elem in auctions:
		try:
			if not elem:
				continue
			delta = elem.auction_end - datetime.datetime.now()

			username = "No Bidders"
			if elem.current_winner:
				username = elem.current_winner.username

			price = "0.00"
			if elem.current_price:
				price = "{0:.2f}".format(elem.current_price)

			result.append({
				'i':str(elem.key().id()), 					# ID
				'a':str(elem.active),						# Is Auction Active? "True" or "False"
				'n':str(elem.item.name),					# Name
				'b':str(elem.item.base_price),				# Base Price
				'u':str(elem.item.product_url),				# Product URL
				'm':str(elem.item.image_url),				# Image URL
				'p':str(price),								# Current Price
				'w':str(username),							# Current Winner Username
				't':str(delta.total_seconds())				# Time Til End (TTE) in Seconds
				})
		except Exception, e:
			logging.error(str(e))

	return result

def auctions_list_all():
	'''
		List all auctions (administrative only)
	'''
	auctions = auction.Auction.get_all()

	if not auctions:
		raise Exception("No auctions in the system.")

	# Build the JSON payload
	result = []
	delta = ""

	for elem in auctions:
		try:
			if not elem:
				continue
			delta = elem.auction_end - datetime.datetime.now()

			result.append({
				'i':str(elem.key().id()), 					# ID
				'a':str(elem.active),						# Is Auction Active? "True" or "False"
				'n':str(elem.item.name),					# Name
				'p':str(elem.item.base_price),				# Base Price
				'u':str(elem.item.product_url),				# Product URL
				'm':str(elem.item.image_url),				# Image URL
				'p':str(elem.current_price),				# Current Price
				'w':str(elem.current_winner.username),		# Current Winner Username
				't':str(delta.total_seconds())				# Time Til End (TTE) in Seconds
				})
		except Exception, e:
			logging.error(str(e))

	return result

def auction_bid(auction_id):
	'''
		Performs a single bid on the given ID if the user has a valid cookie.
	'''
	username = user_controller.validate_cookie()

	if username is None:
		raise Exception("Not logged in!")

	userInfo = user.User.get_by_username(username)

	if userInfo is None:
		raise Exception("Couldn't get info for " + username)

	if userInfo.bid_count <= 0:
		raise Exception("Out of bids!")

	auctionInfo = auction.Auction.get_by_id(int(auction_id))

	if auctionInfo is None or auctionInfo.active is False:
		raise Exception("Auction does not exists.")

	if (auctionInfo.auction_end - datetime.datetime.now()).total_seconds() > 10:
		raise Exception("This auction has not yet started.")

	# Perform Bid:

	userInfo.bid_count -= 1
	userInfo.put()

	auctionInfo.current_winner = userInfo

	# If you ever need to change the time added to an auction when it's bid on
	# THIS is the place to do it.
	auctionInfo.auction_end = datetime.datetime.now() + timedelta(seconds=11)
	auctionInfo.increment_price()
	auctionInfo.put()



def auction_create(item, scheduled_end_time):
	'''
		Schedule an auction to run and end for the specified item at the specified time
		(administrative only)
	'''
	pass

def auction_start(auction_id):
	'''
		Start the specified auction, effective immediately (administrative only)
	'''
	pass

def auction_pause(auction_id):
	'''
		Pause the specified auction indefinitely (administrative only)
	'''
	pass

def auction_end(auction_id):
	'''
		End the specified auction (administrative only)
	'''
	pass

def auction_assign_winner(auction_id, username):
	'''
		Assign the specified user as the winner of the specified auction
		(administrative only)
	'''
	pass