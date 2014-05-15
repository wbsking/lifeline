init = ->
    width = $(window).width()
    $("#header_title").css "margin-left", width/2.5

$ ->
    init()

    $("#header_btn")
        .click ->
            login_text = "登录"
            reg_text = "注册"
            if $(this).attr("login_type") == "0"
                $("#login_div").animate {"height":"360px"}, 300
                $("#email_wrap").show 500
                $(this).attr "login_type", "1"
                $(this).text login_text
                $("#login_btn").text reg_text
            else
                $("#email_wrap").hide 500
                $("#login_div").animate {"height":"270px"}, 300
                $(this).attr "login_type", "0"
                $(this).text reg_text
                $("#login_btn").text login_text

    $("#check_btn")
        .click ->
            do_login true

    $("#login_btn")
        .click ->
            do_login false

    do_login = (remember) ->
            username = $.trim $("#name").val()
            passwd = $.trim $("#passwd").val()
            alert_border = {"border":"1px solid rgba(255, 0, 0, 0.3)"}
            if not username
                $("#name").css alert_border
            if not passwd
                $("#passwd").css alert_border
            if $("#header_btn").attr('login_type') == "1"
                email = $.trim $("#email").val()
                if not email
                    $("#email").css alert_border
                if username and passwd and email
                    passwd = hex_md5 passwd
                    post_data =
                        name: username
                        password: passwd
                        email: email
                        is_remember: remember
                    $.ajax
                        url: "/user/register"
                        type: "POST"
                        data: JSON.stringify(post_data)
                        dataType: "json"
                        success: (data) ->
                            code =  data.code
                            message = data.message
                            if code != 1
                                $("#login_status")
                                    .text "注册失败"
                            else
                                window.location.href = '/'
            else
                if username and passwd
                    passwd = hex_md5 passwd
                    post_data =
                        name: username
                        password: passwd
                        is_remember: remember
                    $.ajax
                        url: "/user/login"
                        type: "POST"
                        data: JSON.stringify(post_data)
                        success: (data) ->
                            code = data.code
                            if code != 1
                                $("#login_status")
                                    .text "登录失败"
                            else
                                window.location.href =  "/"
