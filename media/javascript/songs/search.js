var songlist_reload = function(page_number){
    var approved = $("#song_list_filters_approved").val();
    var search_string = $("#search_filter_input").val();
    
    var unrated = false;
    if ($("#rating_filter_checkboxes_unrated:checked").val() != null)
        unrated = true;
    var hate = false;
    if ($("#rating_filter_checkboxes_hate:checked").val() != null)
        hate = true;
    var meh = false;
    if ($("#rating_filter_checkboxes_meh:checked").val() != null)
        meh = true;
    var known = false;
    if($("#rating_filter_checkboxes_known:checked").val() != null)
        known = true;
    var love = false;
    if($("#rating_filter_checkboxes_love:checked").val() != null)
        love = true;
    if(typeof page_number == 'undefined')
        page_number = 1;
    
    $.getJSON(
        "/song/search/",
        {
           'approved': approved,
           'search_string' : search_string,
           'unrated'    : unrated,
           'hate'       : hate,
           'meh'        : meh,
           'known'      : known,
           'love'       : love,
           'page'       : page_number
        },
        function(data){
                $("#song_list_div").html(data['html']);
                $("#panel_right_content").html("");
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
    });
    $("#rating_filter_checkboxes input").change( function(){
        songlist_reload();
    }
    );
    $("#user_selector_tag").bind("successful_user_change", function(){
        songlist_reload();
    });
});

