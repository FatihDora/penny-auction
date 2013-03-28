PennyAuction = casper.PennyAuction

# define a registration shortcut
PennyAuction.register = (props, failureMessage) ->
    casper.reload ->
        casper.fill "form#registration-form", props, false
        casper.click ".submit-review a.sub-hover"
        casper.waitUntilVisible "#registration-complete", ->
            casper.test.error "Registration was completed successfully, when it shouldn't have"
        , ->
            PennyAuction.expectMessage failureMessage
            casper.test.assertNotVisible "#registration-complete strong",
                "User registration email shouldn't be visible"
        , 500

PennyAuction.registrationProperties = ->
    "FirstName": "Some"
    "LastName": "Dude"
    "Username": "somed00d"
    "Email": "sumd00d@hotmail.com"
    "Password": "asdf123"
    "termsandconditions": true


PennyAuction.test ->
    casper.then ->
        casper.test.comment "Testing bad user registration (missing fields)"
        casper.click "#register-link"
        casper.waitUntilVisible "form#registration-form", ->
            casper.test.assertTitle "Piso Auction - Register",
                "Check page title"

    # without FirstName
    casper.then ->
        casper.test.comment "Without first name"
        props = PennyAuction.registrationProperties()
        delete props["FirstName"]
        PennyAuction.register props, "A First Name is required."

    # without LastName
    casper.then ->
        casper.test.comment "Without last name"
        props = PennyAuction.registrationProperties()
        delete props["LastName"]
        PennyAuction.register props, "A Last Name is required."

    # without Username
    casper.then ->
        casper.test.comment "Without username"
        props = PennyAuction.registrationProperties()
        delete props["Username"]
        PennyAuction.register props, "A username is required."

    # without Email
    casper.then ->
        casper.test.comment "Without email"
        props = PennyAuction.registrationProperties()
        delete props["Email"]
        PennyAuction.register props, "An email address is required."

    # without Password
    casper.then ->
        casper.test.comment "Without password"
        props = PennyAuction.registrationProperties()
        delete props["Password"]
        PennyAuction.register props, "A password is required."

    # without terms & conditions
    casper.then ->
        casper.test.comment "Without terms & conditions"
        props = PennyAuction.registrationProperties()
        delete props["termsandconditions"]
        PennyAuction.register props,
            "You must accept our terms and conditions to register an account."
