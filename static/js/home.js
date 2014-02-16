$(function(){
    $('.comment_info').click(function(){
        if($(this).attr('click')== '0'){
            $(this).attr('click', '1');
            $('.show_comments').show(500);
        }else{
            $(this).attr('click', '0');
            $('.show_comments').hide(500);
        }
    });
    $('#post_dot').click(function(){
        content = $("#new_post_text").val();
        if (!content){
            return
        }
        post_data = {"content":content}
        $.ajax({
            url:"/user/lifedot/create",
            type:"POST",
            data:JSON.stringify(post_data),
            dataType:"json",
            success:function(data){
                var code = data.code;
                if (code == 0){
                    data["content"] = content;
                    $("#new_post_text").val("");
                    line_content = gen_line_content(data);
                    $(".line_content").prepend(line_content);
                }
            }
        });
    });

    var gen_line_content = function(data){
        var create_date = new Date(Date.parse(data.create_time));
        var line_content = data.content;

        create_hours = create_date.getHours() + ":" + create_date.getMinutes() + ":" + create_date.getSeconds();
        create_days = create_date.getDate() + '/' + (create_date.getMonth()+1) + '/' + create_date.getFullYear();
        var comment_count = data.comment_count;
        var dot_id = data.id;
        if(!comment_count){
            comment_count = 0;
        }

        content = '<div class="line_element">\
                        <div class="time_div">\
                            <span class="send_hours">{0}</span>\
                            <span class="send_days">{1}</span>\
                        </div>\
                        <div class="line_gravatar"></div>\
                        <div class="content">\
                            <a class="name" href="/user/lifedot/{2}">{3}</a>\
                        </div>\
                        <div class="line_foot">\
                            <div class="element_info">\
                                <div class="comment_info" click="0">\
                                    <i class="icon-comments-alt"></i>\
                                    <span>{4}</span>\
                                </div>\
                            </div>\
                        </div>\
                    </div>'
        return String.format(content, create_hours, create_days, dot_id, line_content, comment_count);
    }

    String.format = function(){
        if(arguments.length == 0){
            return null;
        }
        var str = arguments[0];
        for(var i=0; i< arguments.length -1; i++){
            var re = new RegExp('\\{'+ i +'\\}', 'gm');
            str = str.replace(re, arguments[i+1]);
        }
        return str;
    }
});
