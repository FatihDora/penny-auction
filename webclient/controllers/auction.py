#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Script passes all currently live auctions to the template.
The template renders the HTML with "loading"                
'''

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template        

class HomeHandler(webapp.RequestHandler):
	def get(self):					
		self.response.out.write(
			template.render('../auction.html', {}))
	def post(self):
		self.redirect('/')
	
def main():
	app = webapp.WSGIApplication([
	  (r'.*', HomeHandler)], debug=True)
	wsgiref.handlers.CGIHandler().run(app)
	
	
if __name__ == "__main__":
	main()