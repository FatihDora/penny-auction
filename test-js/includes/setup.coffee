# define an object for storing shortcuts
PisoAuction = casper.PisoAuction = {}

PisoAuction.test = (testBlock) ->
	casper.start "http://localhost:8081"
	testBlock()
	casper.run ->
		@test.done()

# define a login shortcut
PisoAuction.login = ->
	casper.test.assertTitle "Piso Auction", "Check page title"
	casper.fill "form#login-form",
		"login-username": "kevin"
		"login-password": "asdf",
		true
	casper.test.assertVisible "ul#top-account-info", "Check login successful"
	casper.test.comment "logged in"

# define a logout shortcut
PisoAuction.logout = ->
	casper.test.comment "logged out"
