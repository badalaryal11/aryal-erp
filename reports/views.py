from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from sales.models import Sale, SaleItem
from inventory.models import Product

class ReportDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Total Revenue
        total_revenue = Sale.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        # Total Profit
        # Profit = (Selling Price - Cost Price) * Quantity
        # We need to calculate this from SaleItems
        sale_items = SaleItem.objects.select_related('product')
        total_profit = 0
        for item in sale_items:
            if item.product:
                cost = item.product.cost_price
                revenue = item.total_price
                # Assuming unit_price in SaleItem is the selling price at that time
                # Profit for this item = (Unit Price - Cost Price) * Quantity
                # Note: This uses current cost price. Ideally, we should store cost price at time of sale.
                # For now, using current cost price as per standard simple ERP practice.
                profit = (item.unit_price - cost) * item.quantity
                total_profit += profit
        
        # Top Selling Products
        top_products = SaleItem.objects.values(
            'product__name', 'product__code'
        ).annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum('total_price')
        ).order_by('-total_quantity')[:5]
        
        # Low Stock Products
        low_stock_products = Product.objects.filter(stock_quantity__lt=10).order_by('stock_quantity')[:10]
        
        # Recent Sales
        recent_sales = Sale.objects.order_by('-created_at')[:10]

        context.update({
            'total_revenue': total_revenue,
            'total_profit': total_profit,
            'top_products': top_products,
            'low_stock_products': low_stock_products,
            'recent_sales': recent_sales,
        })
        return context
