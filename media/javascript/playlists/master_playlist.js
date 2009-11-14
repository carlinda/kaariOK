var current_list=-1;
var show_playlist = function(user_id){
    current_list=user_id;
    $.getJSON(
        "/playlist/master_add/"+user_id+"/",
        {},
        function(data){
                $("#playlist_list").html(data['html']);
        }
    );
}

var add_item = function(item_id){
    $.getJSON(
        "/playlist/master/add/"+item_id+"/",
        {},
        function(data){
                $("#master_playlist").html(data['html']);
        }
    );
    if (current_list>-1)
        show_playlist(current_list);
}

var move_up = function(item_id){
    $.getJSON(
        "/playlist/master/move/"+item_id+"/up/",
        {},
        function(data){
                $("#master_playlist").html(data['html']);
        }
    );
}

var move_down = function(item_id){
    $.getJSON(
        "/playlist/master/move/"+item_id+"/down/",
        {},
        function(data){
                $("#master_playlist").html(data['html']);
        }
    );
}

var remove = function(item_id){
    $.getJSON(
        "/playlist/master/remove/"+item_id+"/",
        {},
        function(data){
                $("#master_playlist").html(data['html']);
        }
    );
    if (current_list>-1)
        show_playlist(current_list);
}