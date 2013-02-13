// Generated by CoffeeScript 1.4.0

window.session = {
  init: function(assertion) {
    return jQuery.ajax({
      url: USER_AUTHENTICATE,
      data: {
        assertion: assertion
      },
      success: function(data) {
        var error_message;
        if (data.result) {
          window.user.refresh();
          return window.session.showLoggedIn(data.username);
        } else {
          if (data.error != null) {
            error_message = data.error;
          } else {
            error_message = 'The server could not verify your credentials.';
          }
          return showDialog("error", "Login Failed", error_message);
        }
      }
    });
  },
  showLoggedIn: function(username) {
    return $('#login-wrapper').fadeOut('fast', function() {
      $('.username-label').text(username);
      return $('#logout-wrapper').fadeIn('slow', function() {
        return $('#top-account-info').fadeIn('slow');
      });
    });
  },
  logOut: function() {
    window.session.showLoggedOut();
    return jQuery.ajax({
      url: USER_LOGOUT
    });
  },
  showLoggedOut: function() {
    return $('#logout-wrapper').fadeOut('fast', function() {
      return $('#login-wrapper').fadeIn('slow', function() {
        return $('#top-account-info').fadeOut('slow');
      });
    });
  }
};

$(document).ready(function() {
  navigator.id.watch({
    onlogin: function(assertion) {
      return window.session.init(assertion);
    },
    onlogout: function() {
      return window.session.showLoggedOut();
    }
  });
  $('.persona-login-button').click(function() {
    return navigator.id.request({
      siteName: "Piso Auction"
    });
  });
  return $('#logout-link').click(function(event) {
    event.preventDefault();
    return window.session.logOut();
  });
});
