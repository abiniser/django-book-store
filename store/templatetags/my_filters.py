from django import template
#this fill for makeing your own filter



register = template.Library()


def currency(amount):
    return '{:.2f}'.format(amount) +'$'
register.filter('currency',currency)