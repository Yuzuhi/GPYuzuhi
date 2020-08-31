from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from App.models import YuzuhiUser

REQUIRE_LOGIN_JSON = [
    '/yuzuhi/addtocart/',
    '/yuzuhi/changecartstate/',
    '/yuzuhi/subtocart/',
    '/yuzuhi/makeorder/',
]

REQUIRE_LOGIN = [
    '/yuzuhi/cart/',
    '/yuzuhi/orderdetail/',
    '/yuzuhi/orderlistnotpay/',

]


class LoginMiddleware(MiddlewareMixin):

    def process_request(self, request):

        if request.path in REQUIRE_LOGIN_JSON:

            user_id = request.session.get('user_id')

            if user_id:
                try:
                    user = YuzuhiUser.objects.get(pk=user_id)

                    request.user = user
                    # 如果登陆成功，给request赋予一个user的属性，以后可以通过request.user拿到当前请求级联的用户

                except:
                    # return redirect(reverse('yuzuhi:login'))
                    data = {
                        'status': 302,
                        'msg': 'user not available'
                    }

                    return JsonResponse(data=data)
            else:

                data = {
                    'status': 302,
                    'mgs': 'user_not_login'
                }
                return JsonResponse(data=data)
                # return redirect(reverse('yuzuhi:login'))
        if request.path in REQUIRE_LOGIN:
            user_id = request.session.get('user_id')

            if user_id:
                try:
                    user = YuzuhiUser.objects.get(pk=user_id)

                    request.user = user
                    # 如果登陆成功，给request赋予一个user的属性，以后可以通过request.user拿到当前请求级联的用户
                except:
                    # return redirect(reverse('yuzuhi:login'))
                    return redirect(reverse('yuzuhi:login'))
            else:
                return redirect(reverse('yuzuhi:login'))
                # return redirect(reverse('yuzuhi:login'))
