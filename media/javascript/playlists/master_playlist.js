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