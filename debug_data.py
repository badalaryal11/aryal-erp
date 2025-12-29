
import os
import django
from django.db.models import Sum, F

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from sales.models import Sale
from inventory.models import Product

def check_data():
    print("Checking Product Cost Prices:")
    products = Product.objects.all()[:10]
    for p in products:
        print(f"Product: {p.name}, Price: {p.price}, Cost: {p.cost_price}")

    print("\nChecking Recent Sales:")
    sales = Sale.objects.exclude(total_amount=0).order_by('-created_at')[:10]
    if not sales.exists():
        print("No sales with non-zero total_amount found.")
    
    for s in sales:
        print(f"Sale ID: {s.id}, Amount: {s.total_amount}")
        # Calculate cost for this sale
        cost = 0
        for item in s.items.all():
            c = item.product.cost_price if item.product else 0
            cost += item.quantity * c
            print(f"  - Item: {item.product.name if item.product else 'Unknown'}, Qty: {item.quantity}, Unit Cost: {c}")
        
        print(f"  => Calculated Cost: {cost}, Profit: {s.total_amount - cost}")

if __name__ == "__main__":
    check_data()
