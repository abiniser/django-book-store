from django.urls import path
from checkout import views
from checkout import Webhooks

urlpatterns = [
    path('stripe/config', views.strip_config, name='checkout.strip.config'),
    path('stripe', views.strip_transaction, name='checkout.strip'),
    path('paypal', views.paypal_transaction, name='checkout.paypal'),
    path('stripe/webhook', Webhooks.strip_webhooks, name='checkout.strip'),
]
