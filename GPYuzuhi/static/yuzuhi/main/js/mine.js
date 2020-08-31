function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {   //这部分也可以写在$.ajax里面
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(function () {

    $("#not_login").click(function () {

        window.open('/yuzuhi/login/', target = '_self');

    })

    $("#regis").click(function () {

        window.open('/yuzuhi/register/', target = "_self");

    })

    $("#not_pay").click(function () {

        window.open('/yuzuhi/orderlistnotpay', target = "_self");

    })

    $(document).ready(function () {
        // {# ready事件，指整个html文档渲染完成以后，自动执行的操作。 #}
        // {# 自动执行什么操作？给img标签绑定click事件。 onclick=""; .addEventLisenter("click", function(){}); $().click(); #}
        $('#u_icon').click(function () {
            // {# 只要点击Img，就会触发匿名函数的调用。 #}
            // {# 点击图片。触发input的点击事件。 #}
            $('#icon_upload').click();
        })
    });


})

function upload_icon() {
    // {#alert('你切换图片了');#}
    // {# 主要工作：获取选择的图片内容，读取内容，并将这个图片保存在图像上。 #}
    // {# files: 这个属性就是用来获取input所选择的内容。files[0]就是一个File对象，包含文件的名称、文件的大小、文件的类型等信息。 #}
    var u_icon = $('#icon_upload')[0].files[0];

    // {# 从文件对象img_file中读取图片内容，首先要创建一个文件读取器。 #}
    var reader_file = new FileReader();
    // {# 开始利用文件读取器从img_file中读取内容 #}
    reader_file.readAsDataURL(u_icon);
    // {# 等图片读取完成，reader_file有一个读取成功的自动调用的回调事件 #}
    reader_file.onload = function (ev) {
        $('#u_icon').attr('src', ev.target.result);
        // {# 页面完成头像修改以后，需要将用户在数据库中保存的头像路径也进行修改。需要在views.py中修改用户的u_icon值。 #}
        // {# ajax上传图片文件到django后台：如何使用ajax请求将图片传给django后台的View。 #}
        var formdata = new FormData();
        formdata.append('img_name', u_icon.name);
        formdata.append('u_icon', u_icon);
        // {# 构造表单对象，类似于<form>标签。 #}
        // {# 如果使用ajax发送POST请求，要求携带的参数里面，必须带有csrf这个随机字符串。和<form>的验证原理是一样的。<input type="hidden" name="csrfmiddlewaretoken" value="nzssW2AKQg4OOth2xmYYCYQuPFEAxhkcNPW3wwLQX6CKm8LkWhusgsowh2IcARSN"> #}
        formdata.append('/yuzuhi/changeicon/', '{{ csrf_token }}');
        $.ajax({
            url: "/yuzuhi/changeicon/",
            type: 'POST',
            data: formdata,
            // {# processData：默认值是True，含义就是jQuery会对参数进行编码，让其转化为一个查询字符串。如果为FALSE，意思就是不需要jQuery对data: formdata这个数据做任何处理。 #}
            // {# 查询字符串：一般出现在GET请求中，username='123'&password='456' #}
            processData: false,
            // {# contentType: 该字段指的是此次请求携带的数据是什么累心数据。字段的默认值application/x-www-form-urlencoded。把它的值设置false，目的就是希望不使用默认的值对formdata进行转换。 #}
            contentType: false,
            success: function (data) {
                alert("change success");
            }
        });
        // {# 1. ajax上传文件(图片、文件、音频)需要使用POST请求； #}
        // {# 2. 需要将传给后台的数据，保存在FormData()表单对象中； #}
        // {# 3. POST请求需要携带cstf，ajax请求和<form>请求携带方式不一样； #}
        // {# 4. ajax上传文件的POST请求，需要指定两个参数：processData: false；contentType: false；#}
    }
}