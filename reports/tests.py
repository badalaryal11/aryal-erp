from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from inventory.models import Product, Category
from sales.models import Sale, SaleItem

class ReportDownloadTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_login(self.user)

        # Create dummy data
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product", 
            code="TP1", 
            price=100, 
            cost_price=80, 
            stock_quantity=5, 
            category=self.category
        )
        self.sale = Sale.objects.create(total_amount=200)
        SaleItem.objects.create(
            sale=self.sale,
            product=self.product,
            quantity=2,
            unit_price=100,
            total_price=200
        )

    def test_download_top_selling_csv(self):
        response = self.client.get(reverse('reports:download_top_selling'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        content = response.content.decode('utf-8')
        self.assertIn('Product Name,Product Code,Total Quantity Sold,Total Revenue', content)
        self.assertIn('Test Product,TP1,2,200', content)

    def test_download_low_stock_csv(self):
        response = self.client.get(reverse('reports:download_low_stock'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        content = response.content.decode('utf-8')
        self.assertIn('Product Name,Product Code,Current Stock,Price', content)
        self.assertIn('Test Product,TP1,5,100', content)

    def test_download_recent_sales_csv(self):
        response = self.client.get(reverse('reports:download_recent_sales'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        content = response.content.decode('utf-8')
        self.assertIn('Sale ID,Date,Customer,Total Amount,Payment Method', content)
        # Check for sale ID in content (might need regex if ID is not predictable, but here it's likely 1)
        self.assertIn(str(self.sale.id), content)
