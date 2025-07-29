from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from orders.models import Order
from .models import Payment
import requests

MERCHANT_ID = 'YOUR_MERCHANT_ID'  # Replace with your Zarinpal merchant ID
ZARINPAL_REQUEST_URL = 'https://api.zarinpal.com/pg/v4/payment/request.json'
ZARINPAL_VERIFY_URL = 'https://api.zarinpal.com/pg/v4/payment/verify.json'
ZARINPAL_STARTPAY_URL = 'https://www.zarinpal.com/pg/StartPay/'


def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id, paid=False)
    amount = int(order.get_total_cost())
    description = f'پرداخت سفارش {order.id}'
    callback_url = request.build_absolute_uri('/payment/verify/')
    data = {
        "merchant_id": MERCHANT_ID,
        "amount": amount,
        "callback_url": callback_url,
        "description": description,
        "metadata": {"email": order.email}
    }
    response = requests.post(ZARINPAL_REQUEST_URL, json=data)
    res_data = response.json()['data']
    if response.status_code == 200 and res_data['code'] == 100:
        authority = res_data['authority']
        Payment.objects.create(order=order, authority=authority, amount=amount)
        return redirect(f'{ZARINPAL_STARTPAY_URL}{authority}')
    return render(request, 'payment/error.html', {'error': res_data.get('message', 'خطا در پرداخت')})


def payment_verify(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')
    payment = get_object_or_404(Payment, authority=authority)
    order = payment.order
    if status == 'OK':
        data = {
            "merchant_id": MERCHANT_ID,
            "amount": int(order.get_total_cost()),
            "authority": authority
        }
        response = requests.post(ZARINPAL_VERIFY_URL, json=data)
        res_data = response.json()['data']
        if response.status_code == 200 and res_data['code'] == 100:
            payment.paid = True
            payment.ref_id = res_data['ref_id']
            payment.status = res_data['code']
            payment.save()
            order.paid = True
            order.save()
            return render(request, 'payment/success.html', {'order': order, 'payment': payment})
        else:
            return render(request, 'payment/error.html', {'error': res_data.get('message', 'تراکنش ناموفق بود')})
    return render(request, 'payment/error.html', {'error': 'پرداخت توسط کاربر لغو شد.'})
