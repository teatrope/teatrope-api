from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import Usuario
from rest_framework.authtoken.models import Token


class ContentCrudTests(APITestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(email='u@e.com', password='Secret123!')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_teatro_crud(self):
        list_url = '/api/content/teatros/'
        payload = {
            "nombre": "Teatro Central",
            "descripcion": "Desc",
            "calle": "Av.",
            "distrito": "Centro",
            "latitud": -12.05,
            "longitud": -77.05
        }
        r = self.client.post(list_url, payload, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        teatro_id = r.data['id']
        r2 = self.client.get(f'{list_url}{teatro_id}/')
        self.assertEqual(r2.status_code, status.HTTP_200_OK)

