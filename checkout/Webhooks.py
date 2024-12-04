from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from django_store import settings
from checkout import models
from store.models import Order,Product
from django.core.mail import send_mail
from django.template.loader import render_to_string

@csrf_exempt
def strip_webhooks(request):
    print('Strip Webhooks')
    event = None
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
	#STRIP_SIGNATURE
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
            print('Invalid payload')
            return HttpResponse(status = 400)    
    except stripe.error.SignatureVerificationError as e:
            print('Invalid signature')
            return HttpResponse(status = 400)
    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        print('payment_intent.succeeded')
        transaction_id= payment_intent.metadata.transaction
        print(payment_intent.metadata)
        make_order(transaction_id)


    elif event['type'] == 'payment_method.attached':
        payment_method = event['data']['object']  # contains a stripe.PaymentMethod
            
    else:
        print('Unhandled event type {}'.format(event['type']))
    return HttpResponse(status = 200)   
def make_order(transaction_id): 
    transaction = models.Transaction.objects.get(pk = transaction_id)
    order = Order.objects.create(transaction=transaction)
    products = Product.objects.filter(pk__in = transaction.items)
    for product in products:
        order.orderproduct_set.create(product_id=product.id, price=product.price)
   
    msg_html = render_to_string('emails/order.html', {
        'order': order,
        'products': products
    })
    send_mail(
        subject='New Order',
        html_message=msg_html,
        message=msg_html,
        from_email='kh.hammad2022@gmail.com',
        recipient_list=[transaction.customer_email]
    )
