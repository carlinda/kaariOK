var songlist_reload = function(){
    var approved = $("#song_list_filters_approved").val()
    
    $.getJSON(
        "/song/search/",
        {
           'approved': approved
        },
        function(data){
                $("#song_list_div").html(data['html']);
        }
    );
}

$(document).ready(function(){
    $("#song_list_filters_approved").change( function(){
        songlist_reload();
    }
    );
    $("#search_filter_input").bind("change keyup", function(){
        songlist_reload();
    }
    );
});

