#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template        

class BidPacksHandler(webapp.RequestHandler):
	def get(self):					
		self.response.out.write(
			template.render('../bid_packs.html', {}))
	def post(self):
		self.redirect('/')
	
def main():
	app = webapp.WSGIApplication([
	  (r'.*', BidPacksHandler)], debug=True)
	wsgiref.handlers.CGIHandler().run(app)
	
	
if __name__ == "__main__":
	main()