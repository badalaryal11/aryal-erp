
import os
import django
from django.db.models import Sum

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from sales.models import Sale, SaleItem

def diagnostics():
    print("--- Diagnostics ---")
    sale_count = Sale.objects.count()
    print(f"Total Sales: {sale_count}")
    
    item_count = SaleItem.objects.count()
    print(f"Total Sale Items: {item_count}")
    
    # Check if we have items with price
    items_with_price = SaleItem.objects.filter(total_price__gt=0).count()
    print(f"Items with >0 price: {items_with_price}")
    
    # Check a sample sale
    last_sale = Sale.objects.last()
    if last_sale:
        print(f"Last Sale ID: {last_sale.id}")
        print(f"  Total Amount: {last_sale.total_amount}")
        print(f"  Items Count: {last_sale.items.count()}")
        for item in last_sale.items.all():
            print(f"    - Item: {item.product.name} | Qty: {item.quantity} | Total: {item.total_price}")
            
    # Proposed Fix Check: Calculate what total_amount SHOULD be
    inconsistent_count = 0
    for sale in Sale.objects.all():
        calculated_total = sale.items.aggregate(t=Sum('total_price'))['t'] or 0
        if float(sale.total_amount) != float(calculated_total):
            inconsistent_count += 1
            if inconsistent_count <= 5:
                print(f"Mismatch Sale #{sale.id}: Stored={sale.total_amount}, Calc={calculated_total}")
    
    print(f"Total Inconsistent Sales: {inconsistent_count}")

if __name__ == "__main__":
    diagnostics()
