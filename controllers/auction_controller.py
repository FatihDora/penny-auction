#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import auction, item
from datetime import timedelta
import datetime

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

			result.append({'i':str(elem.key().id()),'p':str(elem.current_price),'w':str(elem.current_winner.username),'t':str(delta.total_seconds())})
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
		raise Exception("No auctions returned.")

	# Build the JSON payload
	result = []
	delta = ""

	for elem in auctions:
		try:
			if not elem:
				continue
			delta = datetime.datetime.now() - elem.auction_end

			result.append({'i':str(elem.key().id()),'p':str(elem.current_price),'w':str(elem.current_winner.username),'t':str(delta.total_seconds())})
		except Exception, e:
			print e

	if result is None:
		raise Exception("There were no auctions for the IDs you provided.")


	return result

def auctions_list_all():
	'''
		List all auctions (administrative only)
	'''
	pass

def auction_create(item, scheduled_start_date):
	'''
		Schedule an auction for the specified item on the specified start date
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
