function message(message, type) {
    var icon = ''
    if (type === "danger") {
        var icon = 'alert-circle';
    }
    if (type === "success") {
        var icon = 'check-circle';
    }
    if (type === "warning") {
        var icon = 'alert-circle';
    }
    let text = '<div class="alert alert-icon alert-pro alert-' + type + ' alert-dismissible" fade in role="alert"><em class="icon ni ni-' + icon + '"></em>' + message + '<button class="close" data-dismiss="alert"></button></div>';
    return text;
}

function clear_errors() {
    $('#info').html("");
    $('#info1').html("");
    $('#info2').html("");
    $('#info3').html("");
    $('#info4').html("");
}

function checkIFLoggedIn() {
    const userData = localStorage.getItem("user_data");
    if (userData == undefined || userData == '' || userData == null) {
        window.location = '/';
    }
}

function checkIFLoggedOut() {
    const userData = localStorage.getItem("user_data");
    if (userData !== null) {
        window.location = '/dashboard.html';
    }
}

function getUserDetails() {
    return JSON.parse(localStorage.getItem("user_data"));
}

$(document).on('click', '#logout', function (event) {
    event.preventDefault();
    localStorage.removeItem("user_data");
    window.location = '/';
});

function notify(title, message, type, position) {
    toastr.clear();
    NioApp.Toast(`<h5>${title}</h5><p>${message}</p>`, type, { position });
}