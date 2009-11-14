var show_playlist = function(user_id){
    $.getJSON(
        "/playlist/min/"+user_id+"/",
        {},
        function(data){
                $("#playlist_list").html(data['html']);
        }
    );
}

var add_song = function(song_id){
    $.getJSON(
        "/playlist/master/add/"+song_id+"/",
        {},
        function(data){
                $("#master_playlist").html(data['html']);
        }
    );
}

var move_up = function(song_id){
    $.getJSON(
        "/playlist/master/move/"+song_id+"/up/",
        {},
        function(data){
                $("#master_playlist").html(data['html']);
        }
    );
}

var move_down = function(song_id){
    $.getJSON(
        "/playlist/master/move/"+song_id+"/down/",
        {},
        function(data){
                $("#master_playlist").html(data['html']);
        }
    );
}

var remove = function(song_id){
    $.getJSON(
        "/playlist/master/remove/"+song_id+"/",
        {},
        function(data){
                $("#master_playlist").html(data['html']);
        }
    );
}