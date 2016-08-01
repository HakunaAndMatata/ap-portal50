$(document).ready(function() {
    if (!user_logged_in) {
        $('#navbar-curriculum').addClass("active");
    }
    else {
        $('#navbar-personal').addClass("active");
        $('.content').css('background-color', bgcolor);
        $('.header').css('background-color', headercolor);
        $('.sidebar').css('background-color', sidecolor);
        $('body').css('color', textcolor);
        $('.name').css('color', textcolor);
    }
});