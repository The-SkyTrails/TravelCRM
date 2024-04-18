// $(function () {
//     var chatarea = $("#chat");
//     console.log("helooooooooooooooooooooooo");


//     $("#chat .message-center a").on("click", function () {
//         console.log("helooo on click.........");
//         var name = $(this).find(".mail-contnet h5").text();
//         var img = $(this).find(".user-img img").attr("src");
//         var id = $(this).attr("data-user-id");
//         var status = $(this).find(".profile-status").attr("data-status");

//         if ($(this).hasClass("active")) {
//             $(this).toggleClass("active");
//             $(".chat-windows #user-chat" + id).hide();
//         } else {
//             $(this).toggleClass("active");
//             if ($(".chat-windows #user-chat" + id).length) {
//                 $(".chat-windows #user-chat" + id)
//                     .removeClass("mini-chat")
//                     .show();
//             } else {
//                 var msg = msg_receive(
//                     "I watched the storm, so beautiful yet terrific."
//                 );
//                 msg += msg_sent("That is very deep indeed!");
//                 var html =
//                     "<div class='user-chat' id='user-chat" +
//                     id +
//                     "' data-user-id='" +
//                     id +
//                     "'>";
//                 html +=
//                     "<div class='chat-head'><img src='" +
//                     img +
//                     "' data-user-id='" +
//                     id +
//                     "'><span class='status " +
//                     status +
//                     "'></span><span class='name'>" +
//                     name +
//                     "</span><span class='opts'><i class='material-icons closeit' data-user-id='" +
//                     id +
//                     "'>clear</i><i class='material-icons mini-chat' data-user-id='" +
//                     id +
//                     "'>remove</i></span></div>";
//                 html +=
//                     "<div class='chat-body'><ul class='chat-list'>" + msg + "</ul></div>";
//                 html +=
//                     "<div class='chat-footer'><input type='text' data-user-id='" +
//                     id +
//                     "' placeholder='Type & Enter' class='form-control'></div>";
//                 html += "</div>";
//                 $(".chat-windows").append(html);
//             }
//         }
//     });

// });


// *******************************************************************
// Chat Application
// *******************************************************************

$(".search-chat").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $(".chat-users li").filter(function () {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});


$(".app-chat .chat-user").on("click", function(event) {
    var $this = $(this);
    
    if ($this.hasClass("active")) {
        return false;
    } else {
        var findChat = $this.attr("data-user-id");
        var findChat2 = $this.attr("user-name");
        console.log("demoooooo",findChat2);
        $(".message-type-box").attr("data-user-id", findChat);
        var personName = $this.find(".chat-title").text();
        
        var personImage = $this.find("img").attr("src");
        if (window.innerWidth <= 767) {
                    $(".chat-container .current-chat-user-name .name").html(
                        personName.split(" ")[0]
                    );
                } else if (window.innerWidth > 767) {
                    $(".chat-container .current-chat-user-name .name").html(personName);
                }
                $(".chat-container .current-chat-user-name img").attr("src", personImage);

        
    }
    if ($this.parents(".user-chat-box").hasClass("user-list-box-show")) {
        $this.parents(".user-chat-box").removeClass("user-list-box-show");
    }
    $(".chat-meta-user").addClass("chat-active");
    $(".chat-send-message-footer").addClass("chat-active");
});




// Send Messages
$(".message-type-box").on("keydown", function (event) {
    if (event.key === "Enter") {
        var message = $(this).val(); 
        var $this = $(this);
        var user_id = $(this).attr("data-user-id");
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: "/get_user_details/", 
            method: "POST", 
            headers: {
                "X-CSRFToken": csrftoken 
            },
            data: { user_id: user_id },
            success: function(response) {
                console.log("Response:", response);
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
            }
        });

        // Start getting time
        var now = new Date();
        var hh = now.getHours();
        var min = now.getMinutes();
        var ampm = hh >= 12 ? "pm" : "am";
        hh = hh % 12;
        hh = hh ? hh : 12;
        hh = hh < 10 ? "0" + hh : hh;
        min = min < 10 ? "0" + min : min;
        var time = hh + ":" + min + " " + ampm;
        // End

        var chatInput = $(this);
        var chatMessageValue = chatInput.val();
        if (chatMessageValue === "") {
            return;
        }
        
        // Determine if the message is sent by the current user or received by the current user
        var isSentByCurrentUser = true; // Assuming the current user is the sender, you need to update this logic based on your authentication system
        
        // Construct the HTML for the message
        var messageClass = isSentByCurrentUser ? 'sent' : 'received';
        var messageHtml = '<div class="chat-message ' + messageClass + '">' +
                            '<div class="message-content">' + chatMessageValue + '</div>' +
                            '<div class="message-time">' + time + '</div>' +
                          '</div>';

        // Append the message to the chat container
        var appendMessage = $(this)
            .parents(".chat-application")
            .find(".active-chat")
            .append(messageHtml);
        
        // Clear the chat input
        var clearChatInput = chatInput.val("");
    }
});




function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}





// *******************************************************************
// Email Application
// *******************************************************************


// $(document).ready(function () {
//     $(".back-btn").click(function () {
//         $(".app-email-chatting-box").hide();
//     });
//     $(".chat-user").click(function () {
//         $(".app-email-chatting-box").show();
//     });
// });


// *******************************************************************
// chat Offcanvas
// *******************************************************************


// $("body").on('click', '.chat-menu', function () {
//     $(".parent-chat-box").toggleClass('app-chat-right');
//     $(this).toggleClass('app-chat-active');
// });