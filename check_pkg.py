
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from sales.models import SaleItem

def check_packaging():
    print("Checking SaleItem packaging data...")
    items = SaleItem.objects.all()
    total = items.count()
    with_pkg = items.filter(packaging__isnull=False).exclude(packaging='').count()
    
    print(f"Total Sale Items: {total}")
    print(f"Items with Parsing: {with_pkg}")
    
    if total > 0:
        print("Sample Data:")
        for item in items[:5]:
            print(f" - Product: {item.product.name} | Pkg: '{item.packaging}' | Product Pkg: '{item.product.packaging if item.product else 'N/A'}'")

if __name__ == "__main__":
    check_packaging()
