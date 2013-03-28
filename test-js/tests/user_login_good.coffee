PennyAuction = casper.PennyAuction

PennyAuction.test ->
	# successful login/logout
	casper.then ->
		casper.test.comment "Testing successful user login"
		# login
		username = "kevin"
		PennyAuction.login username, "asdf", ->
			casper.test.assertNotVisible "#login-wrapper",
				"Login wrapper shouldn't be visible"

			# validate username
			actualUsername = casper.fetchText ".username-label"
			casper.test.assertEquals actualUsername, username, "Check username"

			# logout
			PennyAuction.logout ->
				casper.test.assertVisible "#login-wrapper",
					"Login wrapper should be visible"

