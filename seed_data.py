
import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from sales.models import Sale, SaleItem
from inventory.models import Product

def seed_data():
    print("Seeding sample data...")
    
    # ensure we have products
    products = Product.objects.all()
    if not products.exists():
        print("Creating sample products...")
        p1 = Product.objects.create(name="Laptop", code="LP001", price=100000, cost_price=80000, stock_quantity=10)
        p2 = Product.objects.create(name="Mouse", code="MS001", price=1500, cost_price=800, stock_quantity=50)
        p3 = Product.objects.create(name="Keyboard", code="KB001", price=3000, cost_price=2000, stock_quantity=30)
        products = [p1, p2, p3]
    else:
        print(f"Found {len(products)} products.")
        # Update cost price if 0
        for p in products:
            if p.cost_price == 0:
                p.cost_price = p.price * 0.7 # Mock cost
                p.save()

    # Create sales for last 30 days
    today = timezone.now()
    for i in range(30):
        # 50% chance of sale on any given day
        if random.random() > 0.3:
            date = today - timedelta(days=i)
            
            # Create Sale
            sale = Sale.objects.create(
                customer_name=f"Customer {i}",
                payment_method='CASH'
            )
            sale.created_at = date # Hack to set past date
            sale.save(update_fields=['created_at'])
            
            # Add Items
            total = 0
            for _ in range(random.randint(1, 3)):
                p = random.choice(products)
                qty = random.randint(1, 2)
                item = SaleItem.objects.create(
                    sale=sale,
                    product=p,
                    quantity=qty,
                    unit_price=p.price,
                    total_price=p.price * qty
                )
                total += item.total_price
            
            sale.total_amount = total
            sale.save()
            print(f"Created Sale on {date.date()} for {total}")

    print("Seeding complete.")

if __name__ == "__main__":
    seed_data()
