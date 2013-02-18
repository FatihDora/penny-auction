# define an object for storing shortcuts
PisoAuction = casper.PisoAuction = {}
casper.on "load.finished", ->
  #casper.test.comment "sleeping 250ms"
  casper.wait(250)

PisoAuction.test = (testBlock) ->
	# clear the data
	casper.test.info "Resetting fixtures"
	casper.start "http://localhost:8081/reset_data"
	casper.waitFor ->
		/done/i.test casper.getPageContent()

	# run tests
	casper.thenOpen "http://localhost:8081/"
	testBlock()
	casper.run ->
		@test.done()

# define a login shortcut
PisoAuction.login = (username, password, callback) ->
	casper.test.info "Logging in as '#{username}'"
	casper.test.assertVisible "#login-wrapper",
		"Login wrapper should be visible"
	casper.test.assertNotVisible "#logout-wrapper",
		"Logout wrapper shouldn't be visible"
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
	casper.test.assertNotVisible "#login-wrapper",
		"Login wrapper shouldn't be visible"
	casper.test.assertVisible "#logout-wrapper",
		"Logout wrapper should be visible"
	casper.click "#logout-link"
	casper.waitUntilVisible "#login-wrapper", ->
		casper.test.info "logged out"
		callback()
	, callback

# define a shortcut for expecting certain dialog messages
PisoAuction.expectMessage = (expectedMessage) ->
	casper.test.assertVisible "#messageDialog",
		"Message dialog shown"
	actualMessage = casper.fetchText "#messageDialog p"
	casper.test.assertEquals actualMessage, expectedMessage,
		"Check message"

# define a shortcut for expecting certain dialog partial messages
PisoAuction.expectMessageRegex = (expectedRegex) ->
	casper.test.assertVisible "#messageDialog",
		"Message dialog shown"
	actualMessage = casper.fetchText "#messageDialog p"
	casper.test.assertMatch actualMessage, expectedRegex,
		"Check message (regex)"
