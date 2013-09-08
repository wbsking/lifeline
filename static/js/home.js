$(function(){
    $('#nav_logo').hover(
        function(){
            $('#nav_logo').css("color", "rgb(250, 250, 250)");
        },
        function(){
            $('#nav_logo').css('color', "rgba(240, 240, 240, 0.8)");
    });

    $('#nav_setting_btn').hover(
        function(){
            $(this).css("background", "#5fd3b3");
    },
        function(){
            $(this).css('background', '#36bbce');
        }
    );
});
