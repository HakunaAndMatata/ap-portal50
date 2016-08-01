$(document).ready(function() {
    $('#navbar-settings').addClass('active');
    
    $('.header-default').click(function() {
        defaultHeaderColor();
    });
    
    $('.bg-default').click(function() {
        defaultBGColor();
    });
    
    $('.side-default').click(function() {
        defaultSideColor();
    });
    
    $('.text-default').click(function() {
        defaultTextColor();
    });
    
    $('.btn-save').click(function() {
        save();
    });
});
    
function defaultBGColor() {
    $('#bgcolor-picker').get(0).jscolor.fromString('F0F3F6');
}

function defaultHeaderColor() {
    $('#headercolor-picker').get(0).jscolor.fromString('D7DDE4');
}
    
    
function defaultSideColor() {
    $('#sidecolor-picker').get(0).jscolor.fromString('3A4651');
}
    
function defaultTextColor() {
    $('#textcolor-picker').get(0).jscolor.fromString('4F5F6F');
}
    
function save() {
    var parameters = {
        csrfmiddlewaretoken: csrftoken,
        user: userid,
        bgcolor: $('#bgcolor-picker').val(),
        headercolor: $('#headercolor-picker').val(),
        sidecolor: $('#sidecolor-picker').val(),
        textcolor: $('#textcolor-picker').val(),
        location: $('#location').val(),
        logo: $('#logo').val()
    };
 
     var request = $.ajax({
        url: update_settings_url,
        type: 'POST',
        data: parameters
     });

     request.done(function(response, textStatus, jqXHR) {
        location.reload(true);
     });
     request.fail(function(jqXHR, textStatus, errorThrown) {
        console.log(errorThrown);
     });
}

   