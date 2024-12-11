from django.contrib import admin
from reports.models import OrderReport
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from store.models import Order
from django.db.models.functions import ExtractYear,ExtractWeek,ExtractMonth
from django.db.models import Sum 
import json
# Register your models here.


@admin.register(OrderReport)
class OrderAdmin(admin.ModelAdmin):


    change_list_template= 'admin/reports/orders.html'
 



    def has_change_permission(self, request, obj = None):
        return False
    
    def has_add_permission(self, request):
        return False

def changelist_view(self,request,extra_context = None):
   
    yearly_stats-=(
        Order.objects.select_related('transaction')
        .annotate(year = ExtractYear('crated_at'))
        .values('year')
        .annotate(sum =Sum('transaction_amount'))

    )
    monthly_stats-=(
        Order.objects.select_related('transaction')
        .annotate(month = ExtractMonth('crated_at'))
        .values('year','month')
        .annotate(sum =Sum('transaction_amount'))[:30]

    )
    weekly_stats-=(
        Order.objects.select_related('transaction')
        .annotate(week = ExtractWeek('crated_at'))
        .values('year','month','week')
        .annotate(sum =Sum('transaction_amount'))[:30]

    )
    context ={
        **self.admin_site.each_context(request),
        'yearly_stats':json.dumps(list(yearly_stats)),
        'monthly_stats':json.dumps(list(monthly_stats)), 
        'weekly_stats':json.dumps(list(weekly_stats)),  
        'title':_('Orders Report')
    }

    return TemplateResponse(
        request, self.change_list_templates,context
    )
   