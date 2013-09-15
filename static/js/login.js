$(
    function(){
        width = $(window).width();
        $("#header_title").css({"margin-left":width/2.5});
        $('#check_icon').click(function(){
            if($('#check_icon').attr('check') == '0'){
                $('#check_icon').children().attr('class', 'icon-check');
                $('#check_icon').attr('check', '1');
            }else{
                $('#check_icon').children().attr('class', 'icon-check-empty');
                $('#check_icon').attr('check', '0');
            }
        });
        

        $('#header_btn').click(function(){
            if($(this).attr('login_type') == '0'){
                $("#login_div").animate({'height':"360px"}, 300);
                $("#email_div").show(500);
                $(this).attr('login_type', '1');
                $(this).text("登录");
                $("#login_btn").text("注册");
            }else{
                $("#email_div").hide(500);
                $("#login_div").animate({'height':'270px'}, 300);
                $(this).attr('login_type', '0');
                $(this).text("注册");
                $("#login_btn").text("登录");
            }
        });

        $('#login_btn').click(function(){
            var username = $.trim($('#name').val());
            var passwd = $.trim($('#passwd').val());
            var check = $('#check_icon').attr('check');
            if (!username){
                $('#name').css({'border':'1px solid rgba(255, 0, 0, 0.3)'});
            }
            
            if(!passwd){
                $('#passwd').css({'border':'1px solid rgba(255, 0, 0, 0.3)'});
            }
            
            if ($("#header_btn").attr('login_type') == '1'){
                var email = $.trim($('#email').val());
                if (!email){
                    $('#email').css({'border':'1px solid rgba(255, 0, 0, 0.3)'});
                }
                if (username&&passwd&&email){
                    passwd = hex_md5(passwd);
                    post_data = {"name":username, "password":passwd, "email":email,
                        "platform":"web", "is_remember":check
                    };
                    $.ajax({
                        url:"/user/register",
                        type:"POST",
                        data:JSON.stringify(post_data),
                        dataType:"json",
                        success:function(data){
                            var code = data.code;
                            var message = data.message;
                            if (code!=1){
                                $('#login_status').text(message);
                            }else{
                                window.location.href='/';
                            }
                        }
                    });
                }
            }else{
                if(username&&passwd){
                    passwd = hex_md5(passwd);
                    post_data = {"name":username, "password":passwd, 
                        "platform":"web", "is_remember":check};
                    $.ajax({
                        url:'/user/login',
                        type:'POST',
                        data:JSON.stringify(post_data),
                        success:function(data){
                            var code = data.code;
                            var message = data.message;
                            if (code != 1){
                                $("#login_status").text(message);
                            }else{
                                window.location.href='/';
                            }
                        }});
                    };
            }
        });
    }
);
