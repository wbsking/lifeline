$(function(){
    $('.like_info').hover(function(){
        if($(this).attr('like')=='0'){
            $('.like_info').css({"color":"rgba(255,0,0,1)"});
            $('.like_info i').removeClass("icon-heart-empty");
            $('.like_info i').addClass("icon-heart");
        }
    }, function(){
        if($(this).attr('like')=='0'){
            $('.like_info').css({"color":"rgba(0,0,0,1)"});
            $('.like_info i').removeClass("icon-heart");
            $('.like_info i').addClass("icon-heart-empty");
        }
    });
    $('.like_info').click(function(){
        if($(this).attr('like')=='0'){
            $(this).attr('like', '1');
            $('.like_info').css({"color":"rgba(255,0,0,1)"});
            $('.like_info i').removeClass("icon-heart-empty");
            $('.like_info i').addClass("icon-heart");
        }else{
            $(this).attr('like', '0');
            $('.like_info').css({"color":"rgba(0,0,0,1)"});
            $('.like_info i').removeClass("icon-heart");
            $('.like_info i').addClass("icon-heart-empty");
        }
    });

    $('.comment_info').click(function(){
        if($(this).attr('click')== '0'){
            $(this).attr('click', '1');
            $('.show_comments').show(500);
        }else{
            $(this).attr('click', '0');
            $('.show_comments').hide(500);
        }
    });
});
