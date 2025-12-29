
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from sales.models import SaleItem
from inventory.models import Product

def fix_packaging():
    print("Updating Product Packaging...")
    Product.objects.filter(name='Laptop').update(packaging='Box')
    Product.objects.filter(name='Mouse').update(packaging='Piece')
    Product.objects.filter(name='Keyboard').update(packaging='Box')
    
    print("Updating SaleItem Packaging from Product...")
    items = SaleItem.objects.all()
    count = 0
    for item in items:
        if not item.packaging and item.product:
            item.packaging = item.product.packaging
            item.save()
            count += 1
    print(f"Updated {count} SaleItems.")

if __name__ == "__main__":
    fix_packaging()
