preview = (img, selection) ->
    scaleX = 100 / (selection.width || 1)
    scaleY = 100 / (selection.height || 1)
    p_width = $(img).width()
    p_height = $(img).height()

    $ "#preview"
        .css
            width: Math.round(scaleX*p_width) + 'px'
            height: Math.round(scaleY*p_height) + 'px'
            marginLeft: "-" + Math.round(scaleX*selection.x1) + 'px'
            marginTop: '-' + Math.round(scaleY*selection.y1) + 'px'
    $("input[name='x1']").val selection.x1
    $('input[name="y1"]').val selection.y1
    $('input[name="x2"]').val selection.x2
    $('input[name="y2"]').val selection.y2
    $('input[name="p_width"]').val p_width
    $('input[name="p_height"]').val p_height

$ ->
    $("#modal_link").leanModal {closeButton: ".modal_close"}
    $ ".gra"
        .on "change", "#upload", ->
            $('#modal_link').trigger "click"
            $(".pic_show").imgAreaSelect {handles:true, aspectRatio:'1:1', parent:"#change_size", onSelectChange:preview}
            file_read = window.FileReader
            reader = new FileReader()
            file = this.files[0]
            reader.onload (e) ->
                $('.pic_show_').attr 'src', e.target.result
                $('#preview').attr "src", e.target.result
                if $('form').length > 1
                    f_0 = $ "form:first"
                    f_1 = $ "form:last"
                    f_1.after f_1.clone()
                    f_0.remove()
                    $("form:first").css "display", "none"
                    f_0.after f_0.clone()
                else
                    f_0 = $ "form"
                    f_0.after f_0.clone()
                    $("form:first").css 


