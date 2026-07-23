from django.shortcuts import render, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .mpesa import MpesaClient
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import json

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])

            # Automated Email Notification to Customer
            try:
                subject = f'Order confirmation - Melanin Cake House #{order.id}'
                message = f'Hi {order.first_name},\n\nYour order has been received! ' \
                          f'Order ID: {order.id}\nTotal: KSh {cart.get_total_price()}\n\n' \
                          f'We will notify you once the status changes.'
                send_mail(subject, message, 'sales@melanincakehouse.com', [order.email], fail_silently=True)
            except Exception as e:
                print(f"Email error: {e}")

            # Trigger M-Pesa STK Push
            try:
                mpesa = MpesaClient()
                phone = form.cleaned_data.get('phone_number')
                amount = cart.get_total_price()
                if phone:
                    response = mpesa.stk_push(phone, amount, order.id)
                    # Save the CheckoutRequestID to link it with callback later
                    checkout_id = response.get('CheckoutRequestID')
                    if checkout_id:
                        order.mpesa_checkout_id = checkout_id
                        order.save()
            except Exception as e:
                print(f"M-Pesa STK Push error: {e}")

            cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            result_code = data['Body']['stkCallback']['ResultCode']
            checkout_id = data['Body']['stkCallback']['CheckoutRequestID']

            if result_code == 0:
                # Payment successful
                order = Order.objects.filter(mpesa_checkout_id=checkout_id).first()
                if order:
                    order.paid = True
                    order.status = 'processing'
                    order.save()
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"})
        except Exception as e:
            print(f"Callback error: {e}")
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Error"})
    return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid method"})

def order_track(request):
    order = None
    if 'order_id' in request.GET and 'email' in request.GET:
        order_id = request.GET.get('order_id')
        email = request.GET.get('email')
        try:
            order = Order.objects.get(id=order_id, email=email)
        except Order.DoesNotExist:
            order = None
    return render(request, 'orders/order/track.html', {'order': order})

def check_payment_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return JsonResponse({'paid': order.paid})
