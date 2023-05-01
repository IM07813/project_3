$(document).ready(function() {
    $("#send-btn").click(function() {
        let userInput = $("#user-input").val();
        if (userInput) {
            $("#chat-box").append("<p class='user-message'>" + userInput + "</p>");
            $("#user-input").val("");

            $.post("/get", { query: userInput }, function(data) {
                if (data.response) {
                    $("#chat-box").append("<p class='bot-message'>" + data.response + "</p>");
                } else {
                    $("#chat-box").append("<p class='bot-message'>I'm not sure how to answer that.</p>");
                }
            });
        }
    });

    $("#user-input").keypress(function(e) {
        if (e.which == 13) {
            $("#send-btn").click();
        }
    });
});