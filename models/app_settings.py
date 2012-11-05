#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division
# make string literals be Unicode strings
from __future__ import unicode_literals


class AppSettings(db.Model):
	''' This class stores important global settings for the auction system. '''

	# password hashing settings
	OLD_HASH_WORK_LEVEL = 12
	NEW_HASH_WORK_LEVEL = 12

	# the starting duration of an auction, in seconds
	AUCTION_INITIAL_DURATION = 3600

	# the time added to an auction's duration when a bid is placed, in seconds
	AUCTION_BID_BUMP_TIME = 120

	# the time threshold on an auction below which the autobidder will place bids, in seconds
	AUTOBIDDER_TIME_THRESHOLD = 5
