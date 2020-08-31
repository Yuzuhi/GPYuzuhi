#import sys
#import os
#curPath = os.path.abspath(os.path.dirname(__file__))
#rootPath = os.path.spilt(curPath)[0]
#sys.path.append(rootPath)

import re
import uuid

from alipay import AliPay
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from App.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, YuzuhiUser, Cart, Order, \
    OrderGoods
from App.views_constant import ALL_TYPE, ORDER_TOTAL, ORDER_PRICE_UP, ORDER_PRICE_DOWN, ORDER_SALE_UP, ORDER_SALE_DOWN, \
    HTTP_USER_EXIST, HTTP_CAN_BE_USE, ORDER_STATUS_NOT_PAY, ORDER_STATUS_NOT_RECEIVE, ORDER_STATUS_NOT_SEND
from App.views_helper import  send_email_activate, get_total_price
from GPYuzuhi.settings import MEDIA_KEY_PREFIX, ALIPAY_PUBLIC_KEY, APP_PRIVATE_KEY, ALIPAY_APPID, GOODS_KEY_PREFIX


def hello(request):
    return HttpResponse('世界吹拂着细风')


def index(request):
    return HttpResponse('世界的始焉与终焉')


def home(request):
    main_wheels = MainWheel.objects.all()

    main_navs = MainNav.objects.all()

    main_mustbuys = MainMustBuy.objects.all()

    main_shops = MainShop.objects.all()

    main_shop0_1 = main_shops[0:1]

    main_shop1_3 = main_shops[1:3]

    main_shop3_7 = main_shops[3:7]

    main_shop7_11 = main_shops[7:]

    main_shows = MainShow.objects.all()

    data = {
        "title": "首页",
        "main_wheels": main_wheels,
        "main_navs": main_navs,
        "main_mustbuys": main_mustbuys,
        "main_shops": main_shops,
        "main_shop0_1": main_shop0_1,
        "main_shop1_3": main_shop1_3,
        "main_shop3_7": main_shop3_7,
        "main_shop7_11": main_shop7_11,
        "main_shows": main_shows,
        "GOODS_KEY_PREFIX": GOODS_KEY_PREFIX,
    }
    return render(request, 'main/home.html', context=data)


def market(request):
    return redirect(reverse('yuzuhi:market_with_params',
                            kwargs={"categoryid": 0,
                                    "childcid": 0,
                                    "order_rule": 0,
                                    }))


def market_with_params(request, categoryid, childcid, order_rule):
    foodtypes = FoodType.objects.all()

    # goods_list = Goods.objects.filter(categoryid=typeid).filter(childcid=childcid)

    goods_list = Goods.objects.filter(categoryid=categoryid)

    if childcid == ALL_TYPE:
        pass
    else:
        goods_list = goods_list.filter(childcid=childcid)

    if order_rule == ORDER_TOTAL:
        pass
    elif order_rule == ORDER_PRICE_UP:
        goods_list = goods_list.order_by("price")
    elif order_rule == ORDER_PRICE_DOWN:
        goods_list = goods_list.order_by("-price")
    elif order_rule == ORDER_SALE_UP:
        goods_list = goods_list.order_by("productnum")
    elif order_rule == ORDER_SALE_DOWN:
        goods_list = goods_list.order_by("-productnum")

    foodtype = foodtypes.get(typeid=categoryid)

    """
        全部分类：0#进口水果：103534#国产水果：103533
        切割 #
            ['全部分类：0','进口水果：103534'，'国产水果：103533']
        切割 ：
            [[全部分类,0],[进口水果,103534]，[国产水果,103533]
    """

    foodtypechildnames = foodtype.childtypenames

    foodtypechildname_list = foodtypechildnames.split("#")

    foodtype_childname_list = []

    for foodtypechildname in foodtypechildname_list:
        foodtype_childname_list.append(foodtypechildname.split(':'))

    order_rule_list = [
        ['综合排序', ORDER_TOTAL],
        ['价格升序', ORDER_PRICE_UP],
        ['价格降序', ORDER_PRICE_DOWN],
        ['销量升序', ORDER_SALE_UP],
        ['销量降序', ORDER_SALE_DOWN],
    ]

    data = {
        "title": "闪购",
        "foodtypes": foodtypes,
        "good_list": goods_list,
        "categoryid": int(categoryid),
        'foodtype_childname_list': foodtype_childname_list,
        'childcid': childcid,
        'order_rule_list': order_rule_list,
        'order_rule_view': order_rule,
        "GOODS_KEY_PREFIX": GOODS_KEY_PREFIX,

    }
    return render(request, 'main/market.html', context=data)


def cart(request):
    if request.user.id:
        carts = Cart.objects.filter(c_user=request.user)
        user = request.user
        user_id = request.user.id

        is_all_select = not carts.filter(c_is_select=False).exists()

        data = {
            'title': '购物车',
            'carts': carts,
            'is_all_select': is_all_select,
            'total_price': get_total_price(user_id),
            "user:":user,
            "GOODS_KEY_PREFIX": GOODS_KEY_PREFIX,

        }

        return render(request, 'main/cart.html', context=data)
    else:
        return HttpResponseRedirect(reverse('yuzuhi:login'))


def mine(request):
    user_id = request.session.get("user_id")

    data = {

        'title': '我的',
        'is_login': False,
    }

    if user_id:
        user = YuzuhiUser.objects.get(pk=user_id)
        data['is_login'] = True
        data['username'] = user.u_username
        data['icon'] = MEDIA_KEY_PREFIX + user.u_icon.url
        data['order_not_pay'] = Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NOT_PAY).count()
        data['order_not_receive'] = Order.objects.filter(o_user=user).filter(
            o_status__in=[ORDER_STATUS_NOT_RECEIVE, ORDER_STATUS_NOT_SEND]).count()

    return render(request, 'main/mine.html', context=data)


def register(request):
    if request.method == "GET":

        data = {
            "title": "注册",
        }

        return render(request, "user/register.html", context=data)

    elif request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        email = request.POST.get("email")

        icon = request.FILES.get("icon")

        if not icon:
            icon = "icons/default/R9VPA(Y_G{~C_UE~DD[~F%P.png"

        # password = hash_str(password)

        password = make_password(password)  # 用官方包加密

        user = YuzuhiUser()
        user.u_username = username
        user.u_email = email
        user.u_password = password
        user.u_icon = icon
        user.save()

        u_token = uuid.uuid4().hex

        cache.set(u_token, user.id, timeout=60 * 60 * 24)

        print(u_token)

        send_email_activate(username, email, u_token)

        return redirect(reverse("yuzuhi:login"))
        # return render(request,"")


def check_email(request):
    email = request.GET.get("email")
    result = re.match(r"\w+@\w+\.\w+", email)
    if result:
        data = {
            "status": 200,
            "msg": "email is useable"
        }
    else:
        data = {
            "status": 903,
            "msg": "email is unuseable"
        }
    return JsonResponse(data=data)


def login(request):
    if request.method == "GET":

        error_message = request.session.get('error_message')

        data = {

            "title": "登陆"
        }

        if error_message:
            del request.session['error_message']
            data['error_message'] = error_message

        return render(request, "user/login.html", context=data)

    elif request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        users = YuzuhiUser.objects.filter(u_username=username)

        if users.exists():
            user = users.first()

            if check_password(password, user.u_password):

                if user.is_active:

                    request.session['user_id'] = user.id

                    return redirect(reverse('yuzuhi:mine'))
                else:
                    print("用户未激活")
                    request.session['error_message'] = 'not activate'
                    return redirect(reverse('yuzuhi:login'))
            else:
                print("密码错误")
                request.session['error_message'] = 'password error'
                return redirect(reverse('yuzuhi:login'))

        print("用户不存在")
        request.session['error_message'] = 'user dosen`t exist'
        return redirect(reverse('yuzuhi:login'))


def check_user(request):
    username = request.GET.get("username")

    users = YuzuhiUser.objects.filter(u_username=username)

    data = {
        "status": HTTP_CAN_BE_USE,
        "msg": 'user can be use'
    }

    if users.exists():
        data['status'] = HTTP_USER_EXIST
        data['msg'] = 'user already exist'
    else:
        pass

    return JsonResponse(data=data)


def logout(request):
    request.session.flush()

    return redirect(reverse('yuzuhi:mine'))


def activate(request):
    u_token = request.GET.get('u_token')

    user_id = cache.get(u_token)

    if user_id:
        cache.delete(u_token)

        user = YuzuhiUser.objects.get(pk=user_id)

        user.is_active = True

        user.save()

        return redirect(reverse('yuzuhi:login'))

    return render(request, 'user/activate_fail.html')


def change_icon(request):
    if request.method == "POST":
        icon = request.FILES.get("u_icon")

        user_id = request.session.get("user_id")

        user = YuzuhiUser.objects.get(pk=user_id)

        user.u_icon = icon

        user.save()

        # return HttpResponse(reverse("yuzuhi:change_icon"))

        return redirect(reverse('yuzuhi:mine'))

    return redirect('yuzuhi:login')


def add_to_cart(request):
    goodsid = request.GET.get('goodsid')
    user_id = request.user.id
    carts = Cart.objects.filter(c_user=request.user).filter(c_goods_id=goodsid)

    if carts.exists():
        cart_obj = carts.first()
        cart_obj.c_goods_num = cart_obj.c_goods_num + 1
    else:
        cart_obj = Cart()
        cart_obj.c_goods_id = goodsid
        cart_obj.c_user = request.user

    cart_obj.save()

    print(request.user)

    data = {
        'status': 200,
        'mgs': 'add success',
        'c_goods_num': cart_obj.c_goods_num,
        'total_price': get_total_price(user_id),
    }

    return JsonResponse(data=data)

    # print(request.user)

    # user_id = request.session.get('user_id')
    #
    # if user_id:
    #
    #     return HttpResponse('Add Success')
    # else:
    #
    #     data = {
    #         'status': 302,
    #         "msg": "not login",
    #     }
    #
    #     return JsonResponse(data)
    #     # return redirect(reverse('yuzuhi:login'))

    # ajax无法理解return redirect(reverse('yuzuhi:login'))


def change_cart_state(request):
    # 此处有一个bug，没有判定当前存在的cart_id属于当前登陆的用户
    cart_id = request.GET.get('cartid')
    user_id = request.user.id
    cart_obj = Cart.objects.get(pk=cart_id)

    cart_obj.c_is_select = not cart_obj.c_is_select

    cart_obj.save()

    is_all_select = not Cart.objects.filter(c_user=request.user).filter(c_is_select=False).exists()

    data = {
        'status': 200,
        'msg': 'change ok',
        'c_is_select': cart_obj.c_is_select,
        'is_all_select': is_all_select,
        'total_price': get_total_price(user_id),
    }

    return JsonResponse(data=data)


def sub_to_cart(request):
    goodsid = request.GET.get('goodsid')

    carts = Cart.objects.filter(c_user=request.user).filter(c_goods_id=goodsid)
    user_id = request.user.id
    if carts.exists():
        cart_obj = carts.first()
        if cart_obj.c_goods_num > 0:
            cart_obj.c_goods_num = cart_obj.c_goods_num - 1
            cart_obj.save()

            data = {
                'status': 200,
                'msg': 'add success',
                'c_goods_num': cart_obj.c_goods_num,
                'total_price': get_total_price(user_id),
            }

            return JsonResponse(data=data)


def all_select(request):
    cart_list = request.GET.get('cart_list')
    user_id = request.user.id
    cart_list = cart_list.split("#")

    print(cart_list)

    carts = Cart.objects.filter(id__in=cart_list)

    for cart_obj in carts:
        cart_obj.c_is_select = not cart_obj.c_is_select
        cart_obj.save()

    data = {
        'status': 200,
        'msg': 'ok',
        'total_price': get_total_price(user_id),
    }
    return JsonResponse(data=data)


def delete(request):
    carts_list = request.GET.get('select_list')
    user_id = request.user.id
    print(carts_list)

    carts_list = carts_list.split('#')

    carts = Cart.objects.filter(id__in=carts_list)
    print(carts)
    for cart_obj in carts:
        cart_obj.delete()

    data = {
        'status': 200,
        'msg': 'delete success',
        'total_price': get_total_price(user_id),
    }
    return JsonResponse(data=data)


def make_order(request):
    user_id = request.user.id
    carts = Cart.objects.filter(c_user=request.user).filter(c_is_select=True)

    order = Order()

    order.o_user = request.user

    order.o_price = get_total_price(user_id)

    order.save()

    for cart_obj in carts:
        ordergoods = OrderGoods()
        ordergoods.o_order = order
        ordergoods.o_goods_num = cart_obj.c_goods_num
        ordergoods.o_goods = cart_obj.c_goods
        ordergoods.save()
        cart_obj.delete()

    data = {

        "status": 200,
        "msg": "success",
        'order_id': order.id,
    }

    return JsonResponse(data)


def order_detail(request):
    order_id = request.GET.get('orderid')

    order = Order.objects.get(pk=order_id)

    data = {
        'title': "订单详情",
        'order': order,
        "GOODS_KEY_PREFIX": GOODS_KEY_PREFIX,
    }
    return render(request, 'order/order_detail.html', context=data)


def order_list_not_pay(request):
    orders = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_STATUS_NOT_PAY)

    data = {
        'title': '订单列表',
        'orders': orders,
        "GOODS_KEY_PREFIX": GOODS_KEY_PREFIX,
    }

    return render(request, 'order/order_list_not_pay.html', context=data)


def payed(request):
    order_id = request.GET.get("orderid")

    order = Order.objects.get(pk=order_id)

    order.o_status = ORDER_STATUS_NOT_SEND

    order.save()

    data = {
        'status': 200,
        'msg': 'payed success',
        "orderid": order_id,

    }

    return JsonResponse(data=data)


def alipay(request):
    order_id = request.GET.get("orderid")
    order = Order.objects.get(pk=order_id)
    user = YuzuhiUser.objects.get(pk=order.o_user_id)
    # 构建支付的客户端 AlipayClient
    alipay = AliPay(
        appid=ALIPAY_APPID,
        app_notify_url=None,  # the default notify path
        app_private_key_string=APP_PRIVATE_KEY,
        # alipay public key, do not use your own public key!
        alipay_public_key_string=ALIPAY_PUBLIC_KEY,
        sign_type="RSA2",  # RSA or RSA2
        debug=False  # False by default
    )

    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=order.o_price,
        subject=user.u_username,
        return_url="https://example.com",
        notify_url="https://example.com/notify"  # 可选, 不填则使用默认notify url
    )

    return redirect("https://openapi.alipaydev.com/gateway.do?" + order_string)

# ---------------------------------------------------------------------------------------------------------------------------------

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(levelname)s %(message)s',
#     filemode='a', )
# logger = logging.getLogger('')
#
#
# def alipay(request):
#     # 构建支付的客户端 AlipayClient
#     alipay_client_config = AlipayClientConfig()
#     alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'  # 默认回调url
#     alipay_client_config.app_id = ALIPAY_APPID
#     alipay_client_config.app_private_key = APP_PRIVATE_KEY
#     alipay_client_config.alipay_public_key = ALIPAY_PUBLIC_KEY
#
#     """
#        得到客户端对象。
#        注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
#        logger参数用于打印日志，不传则不打印，建议传递。
#        """
#     client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)
#
#     # 使用Alipay进行支付请求的发起
#
#     """
#        页面接口示例：alipay.trade.page.pay
#     """
#     # 对照接口文档，构造请求对象
#     model = AlipayTradePagePayModel()
#     model.out_trade_no = request.GET.get("orderid")
#     model.total_amount = request.GET.get("ordergoods.o_goods.price")
#     model.subject = "このQRコードはデモです"
#     model.body = "Alipayテスト"
#     model.product_code = "FAST_INSTANT_TRADE_PAY"
#     # settle_detail_info = SettleDetailInfo()
#     # settle_detail_info.amount = 50
#     # settle_detail_info.trans_in_type = "userId"
#     # settle_detail_info.trans_in = "2088302300165604"
#     # settle_detail_infos = list()
#     # settle_detail_infos.append(settle_detail_info)
#     # settle_info = SettleInfo()
#     # settle_info.settle_detail_infos = settle_detail_infos
#     # model.settle_info = settle_info
#     # sub_merchant = SubMerchant()
#     # sub_merchant.merchant_id = "2088301300153242"
#     # model.sub_merchant = sub_merchant
#     request = AlipayTradePagePayRequest(biz_model=model)
#     # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
#     response = client.page_execute(request, http_method="POST")
#
#     print('这里是response', response, "|||||||||")
#     # 客户端操作
#
#     return HttpResponse(response)
#     # return redirect(response)
