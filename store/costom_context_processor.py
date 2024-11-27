from .models import Category
# this fill t not repeat header date in every view def
def website(request):
    categories = Category.objects.order_by('order')
    return {
        'categories':categories
    }