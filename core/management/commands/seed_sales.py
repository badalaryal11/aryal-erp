
from django.core.management.base import BaseCommand
import random
from datetime import timedelta
from django.utils import timezone
from sales.models import Sale, SaleItem
from inventory.models import Product

class Command(BaseCommand):
    help = 'Seeds the database with sample sales data for testing graphs'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding sample data...")
        
        # ensure we have products
        products = Product.objects.all()
        if not products.exists():
            self.stdout.write("Creating sample products...")
            p1 = Product.objects.create(name="Laptop", code="LP001", price=100000, cost_price=80000, stock_quantity=10)
            p2 = Product.objects.create(name="Mouse", code="MS001", price=1500, cost_price=800, stock_quantity=50)
            p3 = Product.objects.create(name="Keyboard", code="KB001", price=3000, cost_price=2000, stock_quantity=30)
            products = [p1, p2, p3]
        else:
            self.stdout.write(f"Found {len(products)} products.")
            # Update cost price if 0 to ensure profit shows up
            for p in products:
                if p.cost_price == 0:
                    p.cost_price = p.price * 0.7  # Mock cost
                    p.save()
                    self.stdout.write(f"Updated cost price for {p.name}")

        # Create sales for last 30 days
        today = timezone.now()
        created_count = 0
        
        for i in range(30):
            # 50% chance of sale on any given day
            if random.random() > 0.3:
                date = today - timedelta(days=i)
                
                # Create Sale
                sale = Sale.objects.create(
                    customer_name=f"Customer {i}",
                    payment_method='CASH'
                )
                sale.created_at = date  # Hack to set past date
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
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f"Successfully created {created_count} sample sales."))
