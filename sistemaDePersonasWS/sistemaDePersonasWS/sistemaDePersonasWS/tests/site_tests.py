from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from sistemaDePersonasApp.models import Person
from datetime import date


class ClientInit(TestCase):
    def setUp(self):
        super(ClientInit, self).setUp()
        self.client = Client()


class HomeTests(ClientInit):
    def test_get_a_person(self):
        a_person = Person.objects.create(first_name='Javier', last_name='Perini', birthday=date.today())
        response = self.client.get(reverse('home'))
        persons = response.context['persons']
        self.assertEqual(persons.first(), a_person)

    def test_no_get_any_person(self):
        response = self.client.get(reverse('home'))
        persons = response.context['persons']
        self.assertEqual(persons.count(), 0)



