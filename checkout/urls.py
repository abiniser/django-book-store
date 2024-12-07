from django.urls import path
from checkout import views
from checkout import Webhooks
from paypal.standard.ipn.views import ipn

urlpatterns = [
    path('stripe/config', views.strip_config, name='checkout.strip.config'),
    path('stripe', views.strip_transaction, name='checkout.strip'),
    path('stripe/webhook', Webhooks.strip_webhooks, name='checkout.strip'),
    path('paypal/webhook',  ipn, name='checkout.paypal-webhook'),
    path('paypal', views.paypal_transaction, name='checkout.paypal'),
]
