$(document).ready(function(){
    $("#song_list_filters_approved").change( function(){
        //Login user here. With an indicator thar the user is changing.
        $.getJSON(
            "/song/search/",
            {
               'approved': $("#song_list_filters_approved").val()
            },
            function(data){
                    $("#song_list_div").html(data['html']);
            }
        );
    }
    );
});