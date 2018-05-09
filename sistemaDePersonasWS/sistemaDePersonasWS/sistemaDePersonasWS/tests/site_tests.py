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


class CreatePersonTests(ClientInit):
    def test_create_a_person(self):
        expect_person_count = Person.objects.count() + 1
        today = date.today().strftime('%d/%m/%Y')
        params = {'first_name': 'Javier', 'last_name': 'Perini', 'birthday': today}
        self.client.post(reverse('create_person'), params)
        self.assertEqual(Person.objects.count(), expect_person_count)

    def test_not_create_a_person_when_last_name_param_is_missing(self):
        expect_person_count = Person.objects.count()
        today = date.today().strftime('%d/%m/%Y')
        params = {'first_name': 'Javier', 'birthday': today}
        self.client.post(reverse('create_person'), params)
        self.assertEqual(Person.objects.count(), expect_person_count)

    def test_redirect_to_home_when_the_creation_was_ok(self):
        today = date.today().strftime('%d/%m/%Y')
        params = {'first_name': 'Javier', 'last_name': 'Perini', 'birthday': today}
        response = self.client.post(reverse('create_person'), params)
        self.assertEqual(response.url, '/')
