#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Script passes all currently live auctions to the template.
The template renders the HTML with "loading"                
'''


import wsgiref.handlers
import random
from datetime import datetime  
from datetime import timedelta
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Auction(db.Model):
	id = db.IntegerProperty()
	name = db.StringProperty()
	productUrl = db.StringProperty()
	imageUrl = db.StringProperty()
	currentPrice = db.FloatProperty()
	currentWinner = db.StringProperty()
	auctionEnd = db.DateTimeProperty()            
	


class HomeHandler(webapp.RequestHandler):
	def get(self):
		populate()
		auctions = db.GqlQuery('SELECT * FROM Auction').fetch(15)
		
		listValues = []
		loggedIn = False
		
		for auction in auctions:
			delta = auction.auctionEnd.replace(microsecond=0) - datetime.now().replace(microsecond=0)
			auction.auctionRemaining = delta
			auction.price = '%.2f' % auction.currentPrice
			listValues.append(auction)
			
		if loggedIn:
			
			user = {'username': 'Bob'}
			values = {
				'auctions': listValues,
				'user': user
				}
		else:
			values = {
				'auctions': listValues
				}	
				
		self.response.out.write(
			template.render('../index.html', values))
	def post(self):
		self.redirect('/')
		

def populate():
	q = db.GqlQuery("SELECT * FROM Auction")
	results = q.fetch(15)
	db.delete(results)
	random.seed()
	auction = Auction(id=1,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=random.uniform(0.0,2.0),currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=random.randint(5,30)))
	auction.put()
	random.seed()
	auction = Auction(id=2,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=random.uniform(0.0,2.0),currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=random.randint(5,30)))
	auction.put()
	random.seed()
	auction = Auction(id=3,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=random.uniform(0.0,2.0),currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=random.randint(5,30)))
	auction.put()
	random.seed()
	auction = Auction(id=4,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=random.uniform(0.0,2.0),currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=random.randint(5,30)))
	auction.put()
	random.seed()
	auction = Auction(id=5,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=random.uniform(0.0,2.0),currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=random.randint(5,30)))
	auction.put()
	random.seed()
	auction = Auction(id=6,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=random.uniform(0.0,2.0),currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=random.randint(5,30)))
	auction.put()
	random.seed()
	auction = Auction(id=7,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=random.uniform(0.0,2.0),currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=random.randint(5,30)))
	auction.put()
	random.seed()
	auction = Auction(id=8,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=random.uniform(0.0,2.0),currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=random.randint(5,30)))
	auction.put()
	random.seed()
	auction = Auction(id=9,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=random.uniform(0.0,2.0),currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=random.randint(5,30)))
	auction.put()
	random.seed()
	auction = Auction(id=10,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=random.uniform(0.0,2.0),currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=random.randint(5,30)))
	auction.put()
	random.seed()
	auction = Auction(id=11,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=random.uniform(0.0,2.0),currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=random.randint(5,30)))
	auction.put()
	random.seed()
	auction = Auction(id=12,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=random.uniform(0.0,2.0),currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=random.randint(5,30)))
	auction.put()
	random.seed()
	auction = Auction(id=13,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=random.uniform(0.0,2.0),currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=random.randint(5,30)))
	auction.put()
	random.seed()
	auction = Auction(id=14,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=random.uniform(0.0,2.0),currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=random.randint(5,30)))
	auction.put()
	random.seed()
	auction = Auction(id=15,name="Senor Gato",productUrl="http://www.google.com",imageUrl="/images/senor_gif.gif",currentPrice=random.uniform(0.0,2.0),currentWinner="darinh",auctionEnd=datetime.now() + timedelta(seconds=random.randint(5,30)))
	auction.put()	
	
def main():
	app = webapp.WSGIApplication([
	  (r'.*', HomeHandler)], debug=True)
	wsgiref.handlers.CGIHandler().run(app)
	
	
if __name__ == "__main__":
	main()