from rest_framework.test import APITestCase
from rest_framework import status
#from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from django.contrib.auth import get_user_model
User = get_user_model()


class AccountsTest(APITestCase):
    def setUp(self):
        pass
    
    def test_post_registration(self):
        response = self.client.post('http://127.0.0.1:8000/accounts/register/',
                                    {'username': 'User10',
                                     'email': 'user10@gmail.com',
                                     'password': 'password',
                                     'password2': 'password'})
        
        user = User.objects.get(username='User10')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.username, 'User10')
        self.assertEqual(user.email, 'user10@gmail.com')

