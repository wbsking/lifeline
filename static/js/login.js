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
        
        $('input').blur(function(){
            if(!$.trim($(this).val())){
                $(this).css({'border':'1px solid rgba(255, 0, 0, 0.4)'});
            }else{
                $(this).css({'border':'1px solid rgba(255, 255, 255, 0.5)'});
            }
        });
        
        $('#login_btn').click(function(){
            var username = $.trim($('#name').val());
            var passwd = $.trim($('#passwd').val());
            
            if (!username){
                $('#name').css({'border':'1px solid rgba(255, 0, 0, 0.3)'});
            }
            
            if(!passwd){
                $('#passwd').css({'border':'1px solid rgba(255, 0, 0, 0.3)'});
            }
            
            
            $.post('/login', {name:username, password:passwd});
        });
    }
)
