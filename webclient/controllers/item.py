#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Script passes all currently live auctions to the template.
The template renders the HTML with "loading"                
'''

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template        

class ItemHandler(webapp.RequestHandler):
	def get(self):					
		self.response.out.write(
			template.render('../item.html', {}))
	def post(self):
		self.redirect('/item')
	
def main():
	app = webapp.WSGIApplication([
	  (r'.*', ItemHandler)], debug=True)
	wsgiref.handlers.CGIHandler().run(app)
	
	
if __name__ == "__main__":
	main()