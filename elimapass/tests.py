from django.test import TestCase
from models import *
import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
def test_tarjeta_valida_y_limite_proporcionado():
    client = APIClient()
    tarjeta = Tarjeta.objects.create(codigo="12345", limite=1000)

    response = client.put(
        reverse('cambiar-limite', args=[tarjeta.codigo]),
        {"limite": 5000},
        format='json'
    )

    assert response.status_code == 200
    assert response.data == {"codigo_tarjeta": tarjeta.codigo, "nuevo_limite": 5000}


