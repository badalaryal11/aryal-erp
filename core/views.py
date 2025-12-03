from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from inventory.models import Product
from sales.models import Sale
from django.db.models import Sum

def home(request):
    total_sales = Sale.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_products = Product.objects.count()
    low_stock_count = Product.objects.filter(stock_quantity__lt=10).count()
    recent_transactions = Sale.objects.order_by('-created_at')[:5]

    context = {
        'total_sales': total_sales,
        'total_products': total_products,
        'low_stock_count': low_stock_count,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'core/home.html', context)

class ContactView(LoginRequiredMixin, TemplateView):
    template_name = 'core/contact.html'
