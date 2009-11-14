var move_up = function(item_id){
    $.getJSON(
        "/playlist/move/"+item_id+"/up/",
        {},
        function(data){
                $("#playlist_div").html(data['html']);
        }
    );
}

var move_down = function(item_id){
    $.getJSON(
        "/playlist/move/"+item_id+"/down/",
        {},
        function(data){
                $("#playlist_div").html(data['html']);
        }
    );
}

var remove = function(item_id){
    $.getJSON(
        "/playlist/remove/"+item_id+"/",
        {},
        function(data){
                $("#playlist_div").html(data['html']);
        }
    );
}

var playlist_reload = function(user_id){
    $.getJSON(
        "/playlist/user/"+user_id+"/",
        {},
        function(data){
                $("#playlist_div").html(data['html']);
        }
    );
}

$(document).ready(function(){
    $("#user_selector_tag").bind("successful_user_change", function(){
        var user_id = $("#user_selector_tag_selector").val();
        playlist_reload(user_id);
    });
});