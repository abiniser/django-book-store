import math
from django.http import JsonResponse,HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django_store import settings
from .forms import UserInfoForm,MyPayPalPaymentForm
from store.models import Product, Cart, Order
from .models import Transaction, PaymentMethod
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
import stripe
from paypal.standard.forms import PayPalPaymentsForm


def strip_config(request):
    return JsonResponse({
        'public_key': settings.STRIPE_PUBLISHABLE_KEY
    })

def strip_transaction(request):
    transaction = make_transaction(request, PaymentMethod.Stripe)
    if not transaction:
        return JsonResponse({
            'message': _('Please enter valid information.')
        }, status=400)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=transaction.amount * 100,
        currency=settings.CURRENCY,
        payment_method_types=['card'],
        metadata={
            'transaction': transaction.id
        }
    )
    return JsonResponse({
        'client_secret': intent['client_secret']
    })


def paypal_transaction(request):
    transaction = make_transaction(request, PaymentMethod.Paypal)
    if not transaction:
        return JsonResponse({
            'message': _('Please enter valid information.')
        }, status=400)
    form = MyPayPalPaymentForm(initial={
        'business':settings.PAYPAL_EMAIL,
        'amount': transaction.amount,
        'invoice':transaction.id,
        'currency_code': settings.CURRENCY,
        'return_url':f'http://{request.get_host()}{reverse("store.checkout_complete")}',
        'cancel_url':f'http://{request.get_host()}{reverse("store.checkout")}',
        'notify_url': f'http://{request.get_host()}{reverse("checkout.paypal-webhook")}'
    })
    return HttpResponse(form.render())








def make_transaction(request, pm):
    form = UserInfoForm(request.POST)
    if form.is_valid():
        cart = Cart.objects.filter(session=request.session.session_key).last()
        products = Product.objects.filter(pk__in=cart.items)
# اذا كانت مطابقة للشروط
        total = 0
        for item in products:
            total += item.price

        if total <= 0:
            return None

        return Transaction.objects.create(
            customer=form.cleaned_data,
            session=request.session.session_key,
            payment_method=pm,
            items=cart.items,
            amount=math.ceil(total)
        )


def send_order_email(order, products):
    msg_html = render_to_string('emails/order.html', {
        'order': order,
        'products': products
    })
    send_mail(
        subject='New Order',
        html_message=msg_html,
        message=msg_html,
        from_email='kh.hammad2022@gmail.com',
        recipient_list=[order.customer['email']]
    )

