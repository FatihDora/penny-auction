#!/usr/bin/env python

import wsgiref.handlers
from datetime import datetime
from datetime import timedelta
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import Auction

class HomeHandler(webapp.RequestHandler):
	def get(self):
		populate()
		auctions = db.GqlQuery('SELECT * FROM Auction ORDER BY auctionEnd DESC').fetch(15)

		listValues = []
		for auction in auctions:
			delta = auction.auctionEnd.replace(microsecond=0) - datetime.now().replace(microsecond=0)
			auction.auctionRemaining = delta
			auction.price = "{0:.2f}".format(auction.currentPrice)
			listValues.append(auction)

		values = {
			'auctions': listValues
		}
		#	delta = auction.auctionEnd

		#values = {
		#	'auctions': auctions
		#}
		self.response.out.write(
			template.render('home.html', values))
	def post(self):
		self.redirect('/')


def populate():
	#q = db.GqlQuery("SELECT * FROM Auction")
	#results = q.fetch(1000)
	#db.delete(results)
	auction = Auction(id=1,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=1.03,currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=10))
	auction.put()
	auction = Auction(id=2,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=2.10,currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=13))
	auction.put()
	auction = Auction(id=3,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=0.32,currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=23))
	auction.put()
	auction = Auction(id=4,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=0.39,currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=8))
	auction.put()
	auction = Auction(id=5,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=2.40,currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=14))
	auction.put()
	auction = Auction(id=6,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=1.20,currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=25))
	auction.put()
	auction = Auction(id=7,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=0.42,currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=22))
	auction.put()
	auction = Auction(id=8,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=0.01,currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=26))
	auction.put()
	auction = Auction(id=9,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=0.93,currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=3))
	auction.put()
	auction = Auction(id=10,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=12.39,currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=9))
	auction.put()
	auction = Auction(id=11,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=3.29,currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=18))
	auction.put()
	auction = Auction(id=12,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=4.20,currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=13))
	auction.put()
	auction = Auction(id=13,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=5.83,currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=2))
	auction.put()
	auction = Auction(id=14,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=8.30,currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=20))
	auction.put()
	auction = Auction(id=15,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=2.09,currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=19))
	auction.put()


def main():
	app = webapp.WSGIApplication([
	  (r'.*', HomeHandler)], debug=True)
	wsgiref.handlers.CGIHandler().run(app)


if __name__ == "__main__":
	main()
