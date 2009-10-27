//Song list row highlighing
$(
    function()
    {
        $("#song_list_table tr").hover(
            function()
            {
                $(this).addClass("highlight");
            },
            function()
            {
                $(this).removeClass("highlight");
            }
        )
    }
);