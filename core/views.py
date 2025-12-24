from django.views.generic import TemplateView
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from inventory.models import Product
from sales.models import Sale
from django.db.models import Sum


@login_required
def home(request):
    context = {
        'total_sales': 0,
        'total_products': 0,
        'low_stock_count': 0,
        'recent_transactions': [],
        'sales_dates': [],
        'sales_amounts': [],
        'error_message': None
    }

    try:
        total_sales = Sale.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_products = Product.objects.count()
        low_stock_count = Product.objects.filter(stock_quantity__lt=10).count()
        recent_transactions = Sale.objects.order_by('-created_at')[:5]

        today = timezone.now()
        
        # --- Helper for Daily Aggregation ---
        def get_daily_sales(days_back):
            start_date = today - timedelta(days=days_back)
            qs = Sale.objects.filter(created_at__gte=start_date).values('created_at', 'total_amount')
            data_map = {}
            for s in qs:
                if not s['created_at']: continue
                date_str = s['created_at'].strftime('%Y-%m-%d')
                data_map[date_str] = data_map.get(date_str, 0) + float(s['total_amount'] or 0)
            
            # Fill in missing dates for continuous line
            sorted_dates = []
            sorted_amounts = []
            for i in range(days_back):
                d = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
                sorted_dates.append(d)
                sorted_amounts.append(data_map.get(d, 0))
            return sorted_dates, sorted_amounts

        # --- Helper for Yearly (Monthly) Aggregation ---
        def get_monthly_sales():
            start_date = today - timedelta(days=365)
            qs = Sale.objects.filter(created_at__gte=start_date).values('created_at', 'total_amount')
            data_map = {}
            for s in qs:
                if not s['created_at']: continue
                # key by Year-Month
                month_key = s['created_at'].strftime('%Y-%m')
                data_map[month_key] = data_map.get(month_key, 0) + float(s['total_amount'] or 0)
            
            # Generate continuous months
            sorted_labels = [] # e.g. "Jan 2024"
            sorted_amounts = []
            current = start_date
            while current <= today:
                m_key = current.strftime('%Y-%m')
                label = current.strftime('%b %Y') # "Dec 2024"
                if not sorted_labels or sorted_labels[-1] != label: # Add unique
                    sorted_labels.append(label)
                    sorted_amounts.append(data_map.get(m_key, 0))
                # Increment roughly a month
                current += timedelta(days=31)
                # Correction to ensure we don't skip or repeat weirdly due to 31 days
                # Simply setting to 1st of next month would be cleaner but loop is acceptable for <12 items
            
            return sorted_labels, sorted_amounts

        # Calculate all datasets
        weekly_dates, weekly_amounts = get_daily_sales(7)
        monthly_dates, monthly_amounts = get_daily_sales(30)
        yearly_labels, yearly_amounts = get_monthly_sales()

        context.update({
            'total_sales': total_sales,
            'total_products': total_products,
            'low_stock_count': low_stock_count,
            'recent_transactions': recent_transactions,
            
            # Pass all datasets
            'weekly_dates': weekly_dates,
            'weekly_amounts': weekly_amounts,
            'monthly_dates': monthly_dates,
            'monthly_amounts': monthly_amounts, 
            'yearly_labels': yearly_labels,
            'yearly_amounts': yearly_amounts,
        })
    except Exception as e:
        print(f"Error in dashboard view: {str(e)}")
        context['error_message'] = f"Dashboard Error: {str(e)}"
        
    return render(request, 'core/home.html', context)

class ContactView(LoginRequiredMixin, TemplateView):
    template_name = 'core/contact.html'
