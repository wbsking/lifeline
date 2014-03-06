$ ->
    $ ".comment_info"
        .click ->
            if $(this).attr "click" == "0"
                $(this).attr "click", "1"
                $ ".show_comments"
                    .show 500
            else
                $(this).attr "click", "0"
                $ ".show_comments"
                    .hide 500
    $ "#post_dot"
        .click ->
            content = $("#new_post_text").val()
            if not content
                return
            post_data =
                content: content
            $.ajax
                url: "/user/lifedot/create"
                type: "POST"
                data: JSON.stringify(post_data)
                dataType: "json"
                success: (data) ->
                    code = data.code
                    if code == 0
                        line_content = data.content
                        $ ".line_content"
                            .prepend line_content
