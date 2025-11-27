from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class SalesAccessTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(username='admin', password='password', is_staff=True)
        self.regular_user = User.objects.create_user(username='user', password='password', is_staff=False)
        self.url = reverse('sales:sale_list')

    def test_anonymous_access(self):
        response = self.client.get(self.url)
        # Should redirect to login
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_regular_user_access(self):
        self.client.force_login(self.regular_user)
        response = self.client.get(self.url)
        # Should be forbidden (403)
        self.assertEqual(response.status_code, 403)

    def test_admin_user_access(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url)
        # Should be allowed (200)
        self.assertEqual(response.status_code, 200)
