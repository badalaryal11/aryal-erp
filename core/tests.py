from django.test import TestCase, Client
from .models import PageView

class PageViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_page_view_creation(self):
        # Simulate a request
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Check if PageView was created
        self.assertTrue(PageView.objects.filter(url='/').exists())
        
        # Check exclusion of admin
        self.client.get('/admin/')
        self.assertFalse(PageView.objects.filter(url='/admin/').exists())

    def test_contact_page(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rampur Ward No.5')
        self.assertContains(response, '9851220582')
        self.assertContains(response, 'aryalagro@gmail.com')
