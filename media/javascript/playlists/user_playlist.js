var move_up = function(song_id){
    $.getJSON(
        "/playlist/move/"+song_id+"/up/",
        {},
        function(data){
                $("#playlist_div").html(data['html']);
        }
    );
}

var move_down = function(song_id){
    $.getJSON(
        "/playlist/move/"+song_id+"/down/",
        {},
        function(data){
                $("#playlist_div").html(data['html']);
        }
    );
}

var remove = function(song_id){
    $.getJSON(
        "/playlist/remove/"+song_id+"/",
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