

# Create your tests here
from django.test import TestCase, Client
from django.urls import reverse

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_link_token(self):
        response = self.client.get(reverse('create_link_token'))
        print("hi")
        self.assertEqual(response.status_code, 200)

    def test_get_access_token(self):
        # Example data for the POST request
        data = {"public_token": "sample_public_token"}
        response = self.client.post(reverse('get-access-token'), data=data, content_type='application/json')
        print("hi")
        self.assertEqual(response.status_code, 200)

    def test_get_auth(self):
        response = self.client.get(reverse('get-auth'))
        print("hi")
        self.assertEqual(response.status_code, 200)

    def test_get_transactions(self):
        response = self.client.get(reverse('get-transactions'))
        print("hi")
        self.assertEqual(response.status_code, 200)
    
    

