var show_playlist = function(user_id){
    $.getJSON(
        "/playlist/min/"+user_id+"/",
        {},
        function(data){
                $("#playlist_list").html(data['html']);
        }
    );
}