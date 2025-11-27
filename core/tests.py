from django.test import TestCase, Client
from .models import PageView

from django.contrib.auth.models import User
from django.urls import reverse

class PageViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_page_view_creation(self):
        self.client.force_login(self.user)
        # Simulate a request
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Check if PageView was created
        self.assertTrue(PageView.objects.filter(url='/', user=self.user).exists())

    def test_admin_path_exclusion(self):
        self.client.force_login(self.user)
        response = self.client.get('/admin/login/')
        # PageView should NOT be created for admin path
        self.assertFalse(PageView.objects.filter(url='/admin/login/').exists())

    def test_contact_page(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rampur Ward No.5')
        self.assertContains(response, '9851220582')
        self.assertContains(response, 'aryalagro.enterprises@gmail.com')

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Password')

    def test_dashboard_data_admin(self):
        # Create dummy data
        from inventory.models import Product, Category
        from sales.models import Sale
        
        category = Category.objects.create(name="Test Category")
        Product.objects.create(name="Test Product", code="TP1", price=100, cost_price=80, stock_quantity=5, category=category)
        Sale.objects.create(total_amount=500)

        # Create and login as admin
        User.objects.create_user(username='admin', password='password', is_staff=True)
        self.client.login(username='admin', password='password')
        
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rs. 500') # Total Sales
        self.assertContains(response, 'Requires attention') # Low stock warning

    def test_dashboard_data_non_admin(self):
        # Create non-admin user
        User.objects.create_user(username='user', password='password')
        self.client.login(username='user', password='password')
        
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Rs. 500') # Should NOT see sales
        self.assertContains(response, 'Welcome to Aryal Agro ERP') # Should see welcome message
