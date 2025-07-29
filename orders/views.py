from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import OrderForm, ShippingForm
from .models import OrderItem, Order
from .tasks import order_created

# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # cart.clear()
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect('orders:shipping_create', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})

def shipping_create(request, order_id):
    cart = Cart(request)
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        shipping_form = ShippingForm(request.POST)
        if shipping_form.is_valid():
            cd = shipping_form.cleaned_data
            shipping_type = cd['shipping_duration']
            shipping = shipping_form.save(commit=False)
            shipping.order = order
            if shipping_type == 'standard':
                shipping.shipping_price = 5.00
            else:
                shipping.shipping_price = 15.50
            shipping.save()
            return render(request, 'orders/verify.html', {'shipping': shipping})
    else:
        shipping_form = ShippingForm()
    return render(request, 'orders/shipping.html', {'order': order, 'shipping_form': shipping_form, 'cart': cart})