function preview(img, selection){
    var scaleX = 100 / (selection.width||1);
    var scaleY = 100 / (selection.height||1);
    var p_width = $(img).width();
    var p_height = $(img).height();
    $("#preview").css({
        width:Math.round(scaleX*p_width)+'px',
        height:Math.round(scaleY*p_height)+'px',
        marginLeft:'-'+Math.round(scaleX*selection.x1)+'px',
        marginTop:'-'+Math.round(scaleY*selection.y1)+'px'
    });
    $('input[name="x1"]').val(selection.x1);
    $('input[name="y1"]').val(selection.y1);
    $('input[name="x2"]').val(selection.x2);
    $('input[name="y2"]').val(selection.y2);
    $('input[name="p_width"]').val(p_width);
    $('input[name="p_height"]').val(p_height);
}

$(function(){
    $("#modal_link").leanModal({closeButton:".modal_close"});
    
    $(".gra").on('change', '#upload', function(){
        $("#modal_link").trigger("click");
        $(".pic_show").imgAreaSelect({handles:true, aspectRatio:'1:1', parent:"#change_size", onSelectChange:preview});
        file_reader = window.FileReader;
        var reader = new FileReader();
        file = this.files[0];
        reader.onload = function(e){
            $(".pic_show").attr("src", e.target.result);
            $("#preview").attr("src", e.target.result);
            if($("form").length > 1){
                var f_0 = $("form:first");
                var f_1 = $("form:last");
                f_1.after(f_1.clone());
                f_0.remove();
                $("form:first").css("display", "none");
            }else{
                var f_0 = $("form");
                f_0.after(f_0.clone());
                $("form:first").css("display", "none");
            }
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

     $("#upload_gra").click(function(){
        var formdata = new FormData($("form:first")[0]);
        $.ajax({
            url:"/image/upload",
            type:"POST",
            data:formdata,
            contentType:false,
            processData:false,
            success:function(data){
                $(".gra_show").attr("src", data);
                $("#dash_gra").attr("src", data);
                $("#change_size").css("display", "none");
                $("#lean_overlay").css("display", "none");
            }
        });
     });
});
