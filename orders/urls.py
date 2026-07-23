from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('track/', views.order_track, name='order_track'),
    path('mpesa-callback/', views.mpesa_callback, name='mpesa_callback'),
    path('check-payment-status/<int:order_id>/', views.check_payment_status, name='check_payment_status'),
]
