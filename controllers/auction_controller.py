#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import auction, item
from datetime import timedelta
import datetime
import logging

from google.appengine.ext import db

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
			delta = datetime.datetime.now() - elem.auction_end
			username = ""
			if elem.current_winner:
				username = elem.current_winner.username

			result.append({'i':str(elem.key().id()),'p':str(elem.current_price),'w':str(username),'t':str(delta.total_seconds())})
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
			delta = datetime.datetime.now() - elem.auction_end

			username = ""
			if elem.current_winner:
				username = elem.current_winner.username

			result.append({
				'i':str(elem.key().id()), 					# ID
				'n':str(elem.item.name),					# Name
				'p':str(elem.item.base_price),				# Base Price
				'u':str(elem.item.product_url),				# Product URL
				'm':str(elem.item.image_url),				# Image URL
				'p':str(elem.current_price),				# Current Price
				'w':str(username),		# Current Winner Username
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
			delta = datetime.datetime.now() - elem.auction_end

			result.append({
				'i':str(elem.key().id()), 					# ID
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
