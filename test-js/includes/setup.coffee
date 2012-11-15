# define an object for storing shortcuts
PisoAuction = casper.PisoAuction = {}

PisoAuction.test = (testBlock) ->
	casper.start "http://localhost:8081"
	casper.reload()
	testBlock()
	casper.run ->
		@test.done()

# define a login shortcut
PisoAuction.login = (username, password, callback) ->
	casper.test.info "Logging in as '#{username}'"
	casper.test.assertVisible "#login-wrapper", "Login wrapper visible"
	casper.test.assertNotVisible "#logout-wrapper", "Logout wrapper not visible"
	casper.fill "form#login-form",
		"login-username": username
		"login-password": password
	, false
	casper.click "#login-submit"
	casper.waitUntilVisible "#logout-wrapper", ->
		casper.test.info "logged in"
		callback()
	, callback

# define a logout shortcut
PisoAuction.logout = (callback) ->
	casper.test.info "Logging out"
	casper.test.assertNotVisible "#login-wrapper", "Login wrapper not visible"
	casper.test.assertVisible "#logout-wrapper", "Logout wrapper visible"
	casper.click "#logout-link"
	casper.waitUntilVisible "#login-wrapper", ->
		casper.test.info "logged out"
		callback()
	, callback

# define a shortcut for expecting certain dialog messages
PisoAuction.expectMessage = (expectedMessage) ->
	casper.test.assertVisible "#messageDialog", "Message dialog shown"
	actualMessage = casper.fetchText "#messageDialog p"
	casper.test.assertEquals actualMessage, expectedMessage, "Check message"
