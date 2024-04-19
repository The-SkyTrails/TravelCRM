$(function () {
    var chatarea = $("#chat");
   


    $("#chat .message-center a").on("click", function () {
        console.log("helooo on click.........");
        var name = $(this).find(".mail-contnet h5").text();
        var img = $(this).find(".user-img img").attr("src");
        var id = $(this).attr("data-user-id");
        var status = $(this).find(".profile-status").attr("data-status");

        if ($(this).hasClass("active")) {
            $(this).toggleClass("active");
            $(".chat-windows #user-chat" + id).hide();
        } else {
            $(this).toggleClass("active");
            if ($(".chat-windows #user-chat" + id).length) {
                $(".chat-windows #user-chat" + id)
                    .removeClass("mini-chat")
                    .show();
            } else {
                var msg = msg_receive(
                    "I watched the storm, so beautiful yet terrific."
                );
                msg += msg_sent("That is very deep indeed!");
                var html =
                    "<div class='user-chat' id='user-chat" +
                    id +
                    "' data-user-id='" +
                    id +
                    "'>";
                html +=
                    "<div class='chat-head'><img src='" +
                    img +
                    "' data-user-id='" +
                    id +
                    "'><span class='status " +
                    status +
                    "'></span><span class='name'>" +
                    name +
                    "</span><span class='opts'><i class='material-icons closeit' data-user-id='" +
                    id +
                    "'>clear</i><i class='material-icons mini-chat' data-user-id='" +
                    id +
                    "'>remove</i></span></div>";
                html +=
                    "<div class='chat-body'><ul class='chat-list'>" + msg + "</ul></div>";
                html +=
                    "<div class='chat-footer'><input type='text' data-user-id='" +
                    id +
                    "' placeholder='Type & Enter' class='form-control'></div>";
                html += "</div>";
                $(".chat-windows").append(html);
            }
        }
    });

});


// *******************************************************************
// Chat Application
// *******************************************************************

$(".search-chat").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $(".chat-users li").filter(function () {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});


// $(".app-chat .chat-user ").on("click", function (event) {
//     console.log("hellllloooooooooooooooooooooo")
//     if ($(this).hasClass(".active")) {
//         return false;
//     } else {
//         var findChat = $(this).attr("data-user-id");
//         var personName = $(this).find(".chat-title").text();
//         var personImage = $(this).find("img").attr("src");
//         var hideTheNonSelectedContent = $(this)
//             .parents(".chat-application")
//             .find(".chat-not-selected")
//             .hide()
//             .siblings(".chatting-box")
//             .show();
//         var showChatInnerContent = $(this)
//             .parents(".chat-application")
//             .find(".chat-container .chat-box-inner-part")
//             .show();

//         if (window.innerWidth <= 767) {
//             $(".chat-container .current-chat-user-name .name").html(
//                 personName.split(" ")[0]
//             );
//         } else if (window.innerWidth > 767) {
//             $(".chat-container .current-chat-user-name .name").html(personName);
//         }
//         $(".chat-container .current-chat-user-name img").attr("src", personImage);
//         $(".chat").removeClass("active-chat");
//         $(".user-chat-box .chat-user").removeClass("bg-light");
//         //$('.chat-container .chat-box-inner-part').css('height', '100%');
//         $(this).addClass("bg-light");
//         $(".chat[data-user-id = " + findChat + "]").addClass("active-chat");
//     }
//     if ($(this).parents(".user-chat-box").hasClass("user-list-box-show")) {
//         $(this).parents(".user-chat-box").removeClass("user-list-box-show");
//     }
//     $(".chat-meta-user").addClass("chat-active");
//     //$('.chat-container').css('height', 'calc(100vh - 158px)');
//     $(".chat-send-message-footer").addClass("chat-active");
// });


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


        $.ajax({
        url: "/get_chat_history/" + findChat + "/",
        method: "GET",
        data: { user_id: findChat },


        });
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
        var $this = $(this);
       
        var user_id = $(this).attr("data-user-id");
        var content = $(this).val(); // Modified to get the value of the input field
        
        
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: "/get_user_details/", 
            method: "POST", 
            headers: {
                "X-CSRFToken": csrftoken 
            },
           data: { 'user_id': user_id,'content':content },
           
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
        $messageHtml =
            '<div class="text-end mb-3"> <div class="p-2 bg-info-subtle text-dark rounded-1 d-inline-block fs-3">' +
            chatMessageValue +
            '</div> <div class="d-block fs-2">' +
            time +
            "</div>  </div>";
        var appendMessage = $(this)
            .parents(".chat-application")
            .find(".active-chat")
            .append($messageHtml);
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


$(document).ready(function () {
    $(".back-btn").click(function () {
        $(".app-email-chatting-box").hide();
    });
    $(".chat-user").click(function () {
        $(".app-email-chatting-box").show();
    });
});


// *******************************************************************
// chat Offcanvas
// *******************************************************************


$("body").on('click', '.chat-menu', function () {
    $(".parent-chat-box").toggleClass('app-chat-right');
    $(this).toggleClass('app-chat-active');
});