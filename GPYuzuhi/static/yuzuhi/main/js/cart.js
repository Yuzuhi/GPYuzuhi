$(function () {

    $(".confirm").click(function () {

        console.log("change state");

        var $confirm = $(this);

        var $li = $confirm.parents("li");

        var cartid = $li.attr('cartid');

        $.getJSON("/yuzuhi/changecartstate/", {'cartid': cartid}, function (data) {
            console.log(data);

            if (data['status'] === 200) {
                $("#total_price").html(data['total_price']);
                if (data['c_is_select']) {
                    $confirm.find("span").find("span").html("√");
                } else {
                    $confirm.find("span").find("span").html("");
                }
                if (data['is_all_select']) {
                    $(".all_select span span").html("√");
                } else {
                    $(".all_select span span").html("");
                }

            }

        })

    })

    $(".subShopping").click(function () {
        console.log("减少一个");

        var $sub = $(this);

        var goodsid = $sub.attr('goodsid');

        $.get('/yuzuhi/subtocart/', {'goodsid': goodsid}, function (data) {
            console.log(data);

            if (data['status'] === 302) {
                window.open('yuzuhi/login/', target = '_self');

            } else if (data['status'] === 200) {
                $sub.next('span').html(data['c_goods_num']);
                $("#total_price").html(data['total_price']);
            }
        })

        // var goodsid = $add.attr("goods");
        // var goodsid = $add.prop("goods");

    })

    $(".addShopping").click(function () {
        console.log("增加一个");

        var $add = $(this);

        // console.log($add);
        // console.log($add.attr('class'));
        // console.log($add.prop('class'));
        //
        // console.log($add.attr('goodsid'));
        // console.log($add.prop('goodsid'));

        var goodsid = $add.attr('goodsid');

        $.get('/yuzuhi/addtocart/', {'goodsid': goodsid}, function (data) {
            console.log(data);

            if (data['status'] === 302) {
                window.open('/yuzuhi/login/', target = '_self');

                // target = '_self' 从当前页面跳转
            } else if (data['status'] === 200) {
                $add.prev('span').html(data['c_goods_num']);
                $("#total_price").html(data['total_price']);

                // $add.prev('span')找到add上一个节点.html(data['c_goods_num']);设置为c_goods_num
            }

        })
    })

    $(".all_select").click(function () {

        var $all_select = $(this);

        var select_list = [];

        var unselect_list = [];

        $(".confirm").each(function () {
            // $(".confirm").each(function () { 遍历confirm中的元素

            var $confirm = $(this);
            // var $confirm = $(this); 记录confirm，用$confirm等于上一行

            var cartid = $confirm.parents("li").attr("cartid");

            if ($confirm.find("span").find("span").html().trim()) {
                // 如果在confirm的span > span中找到内容则为True
                select_list.push(cartid);
                // 类似python append
            } else {
                unselect_list.push(cartid);

            }
        })

        // if(select_list.length > 0 || unselect_list.length > 0){
        //
        // }
        if (unselect_list.length > 0) {
            $.getJSON("/yuzuhi/allselect/", {"cart_list": unselect_list.join("#")}, function (data) {
                console.log(data);
                /*
                由于AJAX不支持传送列表，因此需要对列表用井号连接
                 */
                if (data['status'] === 200) {
                    $(".confirm").find("span").find("span").html("√");
                    $all_select.find("span").find("span").html("√");
                    $("#total_price").html(data['total_price']);
                }
            })
        } else {
            if (select_list.length > 0) {
                $.getJSON("/yuzuhi/allselect/", {"cart_list": select_list.join("#")}, function (data) {
                    console.log(data);
                    if (data['status'] === 200) {
                        $(".confirm").find("span").find("span").html("");
                        $all_select.find("span").find("span").html("");
                        $("#total_price").html(data['total_price']);
                    }

                })
            }

        }

    })

    $(".delete").click(function () {

        var select_list = [];

        $(".confirm").each(function () {
            // $(".confirm").each(function () { 遍历confirm中的元素

            var $confirm = $(this);
            // var $confirm = $(this); 记录confirm，用$confirm等于上一行

            var cartid = $confirm.parents("li").attr("cartid");

            if ($confirm.find("span").find("span").html().trim()) {
                // 如果在confirm的span > span中找到内容则为True
                select_list.push(cartid);
                // 类似python append
            }
        })

        $.getJSON('/yuzuhi/delete/', {'select_list': select_list.join("#")}, function (data) {
            console.log(data);
            if (data['status'] === 200) {
                $(".confirm").each(function () {
                    var $confirm = $(this);
                    if ($confirm.find("span").find("span").html().trim()) {
                        $confirm.parents("li").remove();
                        $("#total_price").html(data['total_price']);
                    }

                })
            }

        })

    })

    $("#make_order").click(function () {

        var select_list = [];

        var unselect_list = [];

        $(".confirm").each(function () {
            // $(".confirm").each(function () { 遍历confirm中的元素

            var $confirm = $(this);
            // var $confirm = $(this); 记录confirm，用$confirm等于上一行

            var cartid = $confirm.parents("li").attr("cartid");

            if ($confirm.find("span").find("span").html().trim()) {
                // 如果在confirm的span > span中找到内容则为True
                select_list.push(cartid);
                // 类似python append
            } else {
                unselect_list.push(cartid);

            }
        })

        if (select_list.length === 0) {
            return
        }

        $.getJSON("/yuzuhi/makeorder/", function (data) {
            console.log(data);

            if (data['status'] === 200) {
                window.open('/yuzuhi/orderdetail/?orderid=' + data['order_id'], target = "_self");
            }

        })
    })

})
