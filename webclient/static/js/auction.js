// Generated by CoffeeScript 1.3.3
(function() {
  var auction;

  $(document).ready(function() {
    return auction.init();
  });

  auction = {
    init: function() {
      callApi(AUCTION_DETAIL, {
        id: auction_id
      }, function(data) {
        var auctions, b, i, ix, m, n, p, t, u, w, _results;
        if (data.result) {
          auctions = data.result;
          if (!(auctions != null)) {
            $("#onecol .gallery").html('<h2 class="red">Auctions</h2><br/><p style="font-size: 14px; width:100%">Unfortunately, there aren\'t any auctions in the system.  To spin up some auctions, visit http://pisoapi.appspot.com/reset_data.</p><br/><br/><br/><div class="clear"></div>');
            return;
          }
          _results = [];
          for (ix in auctions) {
            i = auctions[ix].i;
            n = auctions[ix].n;
            b = auctions[ix].b;
            u = auctions[ix].u;
            m = auctions[ix].m;
            p = auctions[ix].p;
            w = auctions[ix].w;
            t = secondsToHms(auctions[ix].t);
            auction_ids.push(i);
            auction_list[i] = auctions[ix];
            _results.push($("#auctions").append(buildAuction(i, n, b, u, m, p, w, t)));
          }
          return _results;
        }
      });
      return $("#registration-form").submit(function(e) {
        var email, error, first_name, last_name, password, termsaccepted, username;
        e.preventDefault();
        error = "<ul style='clear: both'>";
        first_name = $("#FirstName").val();
        last_name = $("#LastName").val();
        username = $("#Username").val();
        email = $("#Email").val();
        password = $("#Password").val();
        termsaccepted = $("#termsandconditions:checked").val();
        if (first_name.length === 0) {
          error += "<li>A First Name is required.<li/>";
        }
        if (last_name.length === 0) {
          error += "<li>A Last Name is required.<li/>";
        }
        if (username.length === 0) {
          error += "<li>A username is required.<li/>";
        }
        if (email.length === 0) {
          error += "<li>An email address is required.<li/>";
        }
        if (password.length === 0) {
          error += "<li>A password is required.<li/>";
        }
        if (!termsaccepted) {
          error += "<li>You must accept our terms and conditions to register an account.<li/>";
        }
        error += "</ul>";
        if (error !== "<ul style='clear: both'></ul>") {
          showDialog("error", "Registration Error", error);
          return false;
        }
        callApi(USER_REGISTER, {
          first_name: first_name,
          last_name: last_name,
          username: username,
          email: email,
          password: password
        }, function(data) {
          if (data.exception) {
            showDialog("error", "Registration Error", data.exception);
            return;
          }
          if (data.result) {
            $("div#registration-form").slideUp('slow', function() {
              $("div#registration-complete strong").text(email);
              return $("div#registration-complete").fadeIn(1000);
            });
          }
        });
        return false;
      });
    }
  };

}).call(this);
