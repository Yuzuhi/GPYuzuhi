import hashlib

from django.core.mail import send_mail
from django.template import loader

from App.models import Cart
from GPYuzuhi.settings import EMAIL_HOST_USER, SERVER_HOST, SERVER_PORT


def hash_str(source):
    return hashlib.new('sha512', source.encode('utf-8')).hexdigest()


def send_email_activate(username, receive, u_token):
    subject = '%s Yuzuhi_Activate' % username

    from_email = EMAIL_HOST_USER

    recipient_list = [EMAIL_HOST_USER, receive, ]

    data = {

        'username': username,
        'activate_url': 'http://{}:{}/yuzuhi/activate/?u_token={}'.format(SERVER_HOST, SERVER_PORT, u_token)

    }

    html_message = loader.get_template('user/activate.html').render(data)

    send_mail(subject=subject, message='', html_message=html_message, from_email=from_email,
              recipient_list=recipient_list)


def get_total_price(user_id):
    carts = Cart.objects.filter(c_is_select=True).filter(c_user_id=user_id)

    total = 0

    for cart in carts:
        total += cart.c_goods_num * cart.c_goods.price

    return "{:.2f}".format(total)
    # return round(total, 2)
