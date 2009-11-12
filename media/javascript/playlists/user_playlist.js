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
