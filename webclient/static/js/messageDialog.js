$(document).ready(function() {
    $("#messageDialog").dialog({
        autoOpen: false,
        modal: true,
        width: 300,
        height: 200,
        buttons: {
            "Ok": function() {
                $(this).dialog("close");
            }
        }
    });
});

function showDialog(dialogType, title, message) {
    // figure out which icon to use
    var icon = "info";
    switch(dialogType) {
        default:
        case "info":
            icon = "info";
            break;
        case "error":
            icon = "alert";
            break;
    }

    // update the message dialog
    $("#messageDialog p").html(
        "<span class='ui-icon ui-icon-" +
        icon +
        "' style='float:left; margin:0 7px 20px 0;'></span>" +
        message
    );
    $("#messageDialog").dialog({
        title: title
    });

    // show the message dialog
    $("#messageDialog").dialog("open");
}

