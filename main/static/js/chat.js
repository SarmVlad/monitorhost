$(document).ready(function () {
    var msgArea = $('#msgArea');
    var elementMessage = $('#message');
    var webSocket = new WebSocket('ws://' + window.location.host + '/chat/index');
    webSocket.onmessage = function(message) {
        var data = JSON.parse(message.data);
        msgArea.append('<p><strong>'+ data.sender + '</strong>: ' + data.message + '</p>')
    };
    $('#btnSubmit').click(function(e) {
        webSocket.send(elementMessage.val())
    })
});