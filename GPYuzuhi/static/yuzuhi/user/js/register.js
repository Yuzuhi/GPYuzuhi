$(function () {

    var $username = $("#username_input");

    $username.change(function () {

        var username = $username.val().trim(); //   trim()= 去除空格  将输入栏里的值拿到

        if (username.length) {
            //      将用户名发送给服务器进行校验
            $.getJSON('/yuzuhi/checkuser/', {'username': username}, function (data) {
                // 异步
                console.log(data);

                var $username_info = $("#username_info");

                if (data['status'] === 200) {
                    $username_info.html("用户名可用").css("color", "green");
                } else if (data['status'] === 901) {
                    $username_info.html("用户已存在").css("color", "red");
                }

            })

        }

    })

    var $email = $("#email_input");

    $email.change(function () {

        var email = $email.val().trim();

        if (email.length) {

            $.getJSON('/yuzuhi/checkemail', {'email': email}, function (data) {

                console.log(data);

                var $email_info = $("#email_info");

                if (data['status'] === 200) {
                    $email_info.html("");
                } else if (data['status'] === 903) {
                    $email_info.html("请输入正确的邮箱").css("color", "red");
                    return false
                }

            })
        }

    })


})

function check_input() {

    var $username = $("#username_input");

    var username = $username.val().trim();

    if (!username) {
        return false

    }

    var info_color = $("#username_info").css("color");

    console.log(info_color);

    if (info_color == 'rgb(255,0,0)') {
        return false;

    }

    var $password_input = $('#password_input').val().trim();
    if ($password_input.length < 6) {

        return false
    }

    var $password_confirm = $("#password_confirm_input").val().trim();

    if ($password_input == $password_confirm) {

        $password_input = md5($password_input);

        $("#password_input").val($password_input);

        return true

    }


    return false

}

function password_input_confirm() {

    var password_input = $('#password_input').val().trim();
    if (password_input.length < 6) {

        $("#password_length").html("请输入长度大于5的密码").css("color", "red");
    } else {
        $("#password_length").html("");

    }
}

function password_confirm_confirm() {

    var $password_input = $('#password_input').val().trim();

    var $password_confirm = $("#password_confirm_input").val().trim();

    $("#password_confirm_input").change(function () {

        if ($password_input !== $password_confirm) {

            $("#password_info").html("两次输入的密码不一致").css("color", "red");

        } else {
            $("#password_info").html("");
        }
    })
}