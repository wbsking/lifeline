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
            var file = $(":file");
            file.after(file.clone().val(""));
            file.remove();
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
