$(function(){
    $("#modal_link").leanModal({closeButton:".modal_close"});

    $("#upload").change(function(){
        file_reader = window.FileReader;
        var reader = new FileReader();
        file = this.files[0];
        reader.onload = function(e){
            $(".gra_show").attr("src", e.target.result);
        };
        reader.readAsDataURL(file);

    });

    $("#profile_base").click(function(){
        $.ajax({
            type:"GET",
            url:"/user/profile/base",
            dataType:"html",
            success:function(data){
                $("#base_info").html($(data));
            }
        });
    });
    $("#profile_passwd").click(function(){
        $.ajax({
            type:"GET",
            url:"/user/profile/passwd",
            dataType:"html",
            success:function(data){
                $("#base_info").html($(data));
            }
        });
    });
    
    $("#base_save").click(function(){
        $.ajax({
            type:"POST",
            url:"/user/profile",
        });
    });
});
