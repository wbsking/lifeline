$(
    function(){
        $('#check_icon').click(function(){
            if($('#check_icon').attr('check') == '0'){
                $('#check_icon').children().attr('class', 'icon-check');
                $('#check_icon').attr('check', '1');
            }else{
                $('#check_icon').children().attr('class', 'icon-check-empty');
                $('#check_icon').attr('check', '0');
            }
        });
        
        $('#login_btn').mouseover(function(){
            $(this).css({'background':'rgba(240, 240, 240, 0.4)'});
        });
        
        $('#login_btn').mouseout(function(){
            $(this).css({'background':'rgba(180, 180, 180, 0.3)'});
        });
    }
)