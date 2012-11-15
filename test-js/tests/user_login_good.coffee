PisoAuction = casper.PisoAuction

PisoAuction.test ->
	# successful login/logout
	casper.then ->
		casper.test.comment "Testing successful user login"
		#login
		username = "kevin"
		PisoAuction.login username, "asdf", ->
			casper.test.assertNotVisible "#login-wrapper", "Login wrapper not visible"

			# validate username
			actualUsername = casper.fetchText ".username-label"
			casper.test.assertEquals actualUsername, username, "Check username"

			# logout
			PisoAuction.logout ->
				casper.test.assertVisible "#login-wrapper", "Login wrapper visible"

