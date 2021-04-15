$("#loginlink").click(function(){
    $('#signupbox').hide();
    $('#loginbox').show();
});

$(document).ready(function(){
    if ((window.location.pathname).indexOf('login') >= 0) {
        $('#categorybox').css("display", "auto");
    } else {
        $('#signupbox').css("display", "auto");
    }
});