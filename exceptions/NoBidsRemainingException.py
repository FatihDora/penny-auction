class NoBidsRemainingException(Exception):
	''' This exception is thrown if an attempt is made to use bids from an autobidder
	with no remaining bids. The affected_autobidder property stores the autobidder
	which failed. '''

	def __init__(self, autobidder):
		''' Initialize a NoBidsRemainingException. Takes the affected autobidder as
		a parameter. '''

		Exception.__init__(self, u"There are no bids remaining in this auto bidder to use up.")
		self.affected_autobidder = autobidder

