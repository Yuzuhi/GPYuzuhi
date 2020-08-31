$(function () {

    $("#alipay").click(function () {

        console.log("pay");

        var orderid = $(this).attr('orderid');

        $.getJSON("/yuzuhi/payed/", {"orderid": orderid}, function (data) {

            console.log(data);

            if (data['status'] === 200) {

                window.open('/yuzuhi/alipay/?orderid=' + orderid, target = "_self");
            }

        })

    })

})