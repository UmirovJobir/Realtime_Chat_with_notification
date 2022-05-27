from rest_framework.test import APITestCase
from rest_framework import status
#from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Post


class PostTest(APITestCase):
    def setUp(self):
        password = make_password('password')
        self.user1 = User.objects.create(username='User1', email='user1@gmail.com', password=password)
        self.user2 = User.objects.create(username='User2', email='user2@gmail.com', password=password)
        self.user3 = User.objects.create(username='User3', email='user3@gmail.com', password=password)
        
        Post.objects.create(title='title1', body='body1', author=self.user1)
        Post.objects.create(title='title2', body='body2', author=self.user2)
        Post.objects.create(title='title3', body='body3', author=self.user3)
    
    def test_get_list(self):
        response = self.client.get('http://127.0.0.1:8000/blog/post/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_retrieve(self):
        #self.authorization_activate()
        response = self.client.get('http://127.0.0.1:8000/blog/post/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('title1', response.data['title'])
        self.assertEqual('body1', response.data['body'])
    
    def authorization_activate(self):
        token_response = self.client.post('http://127.0.0.1:8000/accounts/api/token/', {'username': 'User1',
                                                                             'password': 'password'}, 
                               format='json')
        self.access_token = token_response.data['access']
        self.refresh_token = token_response.data['refresh']
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    
    def test_update_with_auth(self):
        self.authorization_activate()
        response = self.client.put('http://127.0.0.1:8000/blog/post/1/', {'title': 'Changed title',
                                                                          'body': 'Changed body'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('Changed title', response.data['title'])
        self.assertEqual('Changed body', response.data['body'])
    
    def test_partial_update_with_auth(self):
        self.authorization_activate()
        response = self.client.patch('http://127.0.0.1:8000/blog/post/1/', {'title': 'Changed title 2'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('Changed title 2', response.data['title'])
    
    def test_update_without_auth(self):
        response = self.client.put('http://127.0.0.1:8000/blog/post/1/', {'title': 'Changed title',
                                                                          'body': 'Changed body'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_partial_update_without_auth(self):
        response = self.client.patch('http://127.0.0.1:8000/blog/post/1/', {'title': 'Changed title 2'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_with_incorrect_auth(self):
        self.authorization_activate()
        response = self.client.put('http://127.0.0.1:8000/blog/post/2/', {'title': 'Changed title',
                                                                          'body': 'Changed body'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_partial_update_with_incorrect_auth(self):
        self.authorization_activate()
        response = self.client.patch('http://127.0.0.1:8000/blog/post/2/', {'title': 'Changed title 2'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_with_auth(self):
        self.authorization_activate()
        response = self.client.post('http://127.0.0.1:8000/blog/post/', {'title': 'New title',
                                                                          'body': 'New body'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual('New title', response.data['title'])
        self.assertEqual('New body', response.data['body'])
    
    def test_create_without_auth(self):
        response = self.client.post('http://127.0.0.1:8000/blog/post/', {'title': 'New title',
                                                                          'body': 'New body'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_destroy_without_auth(self):
        response = self.client.delete('http://127.0.0.1:8000/blog/post/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_destroy_with_auth(self):
        self.authorization_activate()
        response = self.client.delete('http://127.0.0.1:8000/blog/post/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        
