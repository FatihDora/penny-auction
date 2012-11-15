PisoAuction = casper.PisoAuction

# define a registration shortcut
PisoAuction.register = (props, failureMessage) ->
    casper.reload ->
        casper.fill "form#registration-form", props, false
        casper.click ".submit-review a.sub-hover"
        casper.waitUntilVisible "#registration-complete", ->
            casper.test.error "Registration was completed successfully, when it shouldn't have"
        , ->
            PisoAuction.expectMessage failureMessage
            casper.test.assertNotVisible "#registration-complete strong",
                "User registration email shouldn't be visible"
        , 500

PisoAuction.registrationProperties = ->
    "FirstName": "Some"
    "LastName": "Dude"
    "Username": "somed00d"
    "Email": "sumd00d@hotmail.com"
    "Password": "asdf123"
    "termsandconditions": true


PisoAuction.test ->
    casper.then ->
        casper.test.comment "Testing bad user registration (missing fields)"
        casper.click "#register-link"
        casper.waitUntilVisible "form#registration-form", ->
            casper.test.assertTitle "Piso Auction - Register",
                "Check page title"

    # without FirstName
    casper.then ->
        casper.test.comment "Without first name"
        props = PisoAuction.registrationProperties()
        delete props["FirstName"]
        PisoAuction.register props, "A First Name is required."

    # without LastName
    casper.then ->
        casper.test.comment "Without last name"
        props = PisoAuction.registrationProperties()
        delete props["LastName"]
        PisoAuction.register props, "A Last Name is required."

    # without Username
    casper.then ->
        casper.test.comment "Without username"
        props = PisoAuction.registrationProperties()
        delete props["Username"]
        PisoAuction.register props, "A username is required."

    # without Email
    casper.then ->
        casper.test.comment "Without email"
        props = PisoAuction.registrationProperties()
        delete props["Email"]
        PisoAuction.register props, "An email address is required."

    # without Password
    casper.then ->
        casper.test.comment "Without password"
        props = PisoAuction.registrationProperties()
        delete props["Password"]
        PisoAuction.register props, "A password is required."

    # without terms & conditions
    casper.then ->
        casper.test.comment "Without terms & conditions"
        props = PisoAuction.registrationProperties()
        delete props["termsandconditions"]
        PisoAuction.register props,
            "You must accept our terms and conditions to register an account."
