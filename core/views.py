from django.views.generic import TemplateView
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from inventory.models import Product
from sales.models import Sale
from django.db.models import Sum
from django.db.models.functions import TruncDay

@login_required
def home(request):
    total_sales = Sale.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_products = Product.objects.count()
    low_stock_count = Product.objects.filter(stock_quantity__lt=10).count()
    recent_transactions = Sale.objects.order_by('-created_at')[:5]

    today = timezone.now()
    last_30_days = today - timedelta(days=30)
    
    daily_sales = Sale.objects.filter(
        created_at__gte=last_30_days
    ).annotate(
        day=TruncDay('created_at')
    ).values('day').annotate(
        total=Sum('total_amount')
    ).order_by('day')

    sales_dates = [item['day'].strftime('%Y-%m-%d') for item in daily_sales]
    sales_amounts = [float(item['total']) for item in daily_sales]

    context = {
        'total_sales': total_sales,
        'total_products': total_products,
        'low_stock_count': low_stock_count,
        'recent_transactions': recent_transactions,
        'sales_dates': sales_dates,
        'sales_amounts': sales_amounts,
    }
    return render(request, 'core/home.html', context)

class ContactView(LoginRequiredMixin, TemplateView):
    template_name = 'core/contact.html'
