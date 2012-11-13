PisoAuction = casper.PisoAuction

# define a registration shortcut
PisoAuction.register = (props) ->
	casper.then ->
		casper.click "#login-wrapper a"
	casper.then ->
		casper.test.assertTitle "Piso Auction - Register", "Check page title"
		casper.fill "#registration-form", props, true

PisoAuction.test ->
	casper.test.comment "Testing user registration"
	PisoAuction.register
		"FirstName": "Some"
		"LastName": "Dude"
		"Username": "somed00d"
		"Email": "sumd00d@hotmail.com"
		"Password": "asdf123"
		"termsandconditions": true
	casper.then ->
		casper.test.assertVisible "#registration-complete",
			"Check registration successful"
