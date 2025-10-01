from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Usuario


class AuthTests(APITestCase):
    def test_register_and_login(self):
        url_register = reverse('usuario-register')
        data = {"email": "user@example.com", "password": "Secret123!", "tipo_rol": "CONSUMIDOR"}
        resp = self.client.post(url_register, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        token = resp.data['token']
        self.assertTrue(token)

        url_login = reverse('usuario-login')
        resp2 = self.client.post(url_login, {"email": "user@example.com", "password": "Secret123!"}, format='json')
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)

