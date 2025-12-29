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
@login_required
def home(request):
    context = {
        'total_sales': 0,
        'total_products': 0,
        'low_stock_count': 0,
        'recent_transactions': [],
        'sales_dates': [],
        'sales_amounts': [],
        'profit_amounts': [],  # Added for profit
        'error_message': None
    }

    try:
        total_sales = Sale.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_products = Product.objects.count()
        low_stock_count = Product.objects.filter(stock_quantity__lt=10).count()
        recent_transactions = Sale.objects.order_by('-created_at')[:5]

        today = timezone.now()
        
        # --- Helper for Daily Aggregation ---
        from django.db.models import F
        
        def get_daily_data(days_back):
            start_date = today - timedelta(days=days_back)
            # Annotate each sale with its total cost
            qs = Sale.objects.filter(created_at__gte=start_date).annotate(
                total_cost=Sum(F('items__quantity') * F('items__product__cost_price'))
            ).values('created_at', 'total_amount', 'total_cost')
            
            sales_map = {}
            profit_map = {}
            
            for s in qs:
                if not s['created_at']: continue
                date_str = s['created_at'].strftime('%Y-%m-%d')
                
                amount = float(s['total_amount'] or 0)
                cost = float(s['total_cost'] or 0)
                profit = amount - cost
                
                sales_map[date_str] = sales_map.get(date_str, 0) + amount
                profit_map[date_str] = profit_map.get(date_str, 0) + profit
            
            # Fill in missing dates for continuous line
            sorted_dates = []
            sorted_sales = []
            sorted_profit = []
            
            for i in range(days_back):
                d = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
                sorted_dates.append(d)
                sorted_sales.append(sales_map.get(d, 0))
                sorted_profit.append(profit_map.get(d, 0))
                
            return sorted_dates, sorted_sales, sorted_profit

        # --- Helper for Yearly (Monthly) Aggregation ---
        def get_monthly_data():
            start_date = today - timedelta(days=365)
            qs = Sale.objects.filter(created_at__gte=start_date).annotate(
                total_cost=Sum(F('items__quantity') * F('items__product__cost_price'))
            ).values('created_at', 'total_amount', 'total_cost')
            
            sales_map = {}
            profit_map = {}
            
            for s in qs:
                if not s['created_at']: continue
                # key by Year-Month
                month_key = s['created_at'].strftime('%Y-%m')
                
                amount = float(s['total_amount'] or 0)
                cost = float(s['total_cost'] or 0)
                profit = amount - cost

                sales_map[month_key] = sales_map.get(month_key, 0) + amount
                profit_map[month_key] = profit_map.get(month_key, 0) + profit
            
            # Generate continuous months
            sorted_labels = [] # e.g. "Jan 2024"
            sorted_sales = []
            sorted_profit = []
            
            current = start_date
            while current <= today:
                m_key = current.strftime('%Y-%m')
                label = current.strftime('%b %Y') # "Dec 2024"
                if not sorted_labels or sorted_labels[-1] != label: # Add unique
                    sorted_labels.append(label)
                    sorted_sales.append(sales_map.get(m_key, 0))
                    sorted_profit.append(profit_map.get(m_key, 0))
                # Increment roughly a month
                current += timedelta(days=31)
            
            return sorted_labels, sorted_sales, sorted_profit

        # Calculate all datasets
        weekly_dates, weekly_sales, weekly_profit = get_daily_data(7)
        monthly_dates, monthly_sales, monthly_profit = get_daily_data(30)
        yearly_labels, yearly_sales, yearly_profit = get_monthly_data()

        context.update({
            'total_sales': total_sales,
            'total_products': total_products,
            'low_stock_count': low_stock_count,
            'recent_transactions': recent_transactions,
            
            # Pass all datasets
            'weekly_dates': weekly_dates,
            'weekly_amounts': weekly_sales,
            'weekly_profit': weekly_profit,
            
            'monthly_dates': monthly_dates,
            'monthly_amounts': monthly_sales, 
            'monthly_profit': monthly_profit,
            
            'yearly_labels': yearly_labels,
            'yearly_amounts': yearly_sales,
            'yearly_profit': yearly_profit,
        })
    except Exception as e:
        print(f"Error in dashboard view: {str(e)}")
        context['error_message'] = f"Dashboard Error: {str(e)}"
        
    return render(request, 'core/home.html', context)

class ContactView(LoginRequiredMixin, TemplateView):
    template_name = 'core/contact.html'
