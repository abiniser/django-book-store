from django.shortcuts import render
from .models import Cart, Product,Category,Author,Order,OrderProduct,Slider
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.translation import gettext 
from django.core.mail import send_mail
from django.template.loader import render_to_string
# Create your views here.
def index(request):
    products = Product.objects.select_related('author').filter(featured = True)
    slides = Slider.objects.order_by('order') # order by is for sorting row base on other like id or other
    return render( request, 'index.html',
                {
                'products' : products,
                'slides' : slides
                }
                  )




def product(request,pid):
     # product have product id
     products = Product.objects.get(pk =pid)
     return render(
          request,'product.html',
          {
               'product' : product
          }
     )




def category (request,cid=None):
     cat =None
     query = request.GET.get('query')
     cid = request.GET.get('category',cid)
     where={}

     if cid :
          cat = Category.objects.get(pk = cid)
          where['category_id']=cid
     if query:
          where['name__icontains'] = query

     products= Product.objects.filter(**where) 
     paginator = Paginator(products,9)  
     page_number = request.GET.get('page') 
     page_obj = paginator.get_page(page_number)   
     return render(

          request,'category.html',{
          'page_obj':page_obj,
          "category": cat
          }
     )




def cart (request):
     return render(
          request,'cart.html'
     )
def cart_update(request, pid):
     if not request.session.session_key:
          request.session.create()

     session_id = request.session.session_key
     cart_model = Cart.objects.filter( session = session_id).last()
     if cart_model is None:
          cart_model = Cart.objects.create(session_id = session_id, items=[pid] )
     elif pid not in cart_model.items:
          cart_model.items.append(pid)
          cart_model.save()
     return JsonResponse({
          'message' :('The product has been added you your cart.'),
          'items_count': len(cart_model.items)
     })

def cart_remove(request, pid):
     session_id = request.session.session_key
     
     if not session_id:
          return JsonResponse({})

     cart_model = Cart.objects.filter( session = session_id).last()
     if cart_model is None:
          cart_model = Cart.objects.create(session_id = session_id, items=[pid] )
     elif pid in cart_model.items:
          cart_model.items.remove(pid)
          cart_model.save()
     return JsonResponse({
          'message' :('The product has been removed from you your cart.'),
          'items_count': len(cart_model.items)
     })




def checkout (request):
     return render(
          request,'checkout.html'
     )



def checkout_complete (request):
     return render(
          request,'checkout-complete.html'
     )

def send_order_email(order,products):
     msg_html = render_to_string('emails/order.html')
     send_mail(subject='New Order',
               html_message=msg_html,
               message=msg_html,
               from_email='noreeply@example.com',
               recipient_list=['customer@example.com']
               
               )
     

