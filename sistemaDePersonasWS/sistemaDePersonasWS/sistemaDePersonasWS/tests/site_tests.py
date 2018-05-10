from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from sistemaDePersonasApp.models import Person, PersonImages
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile


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


class UploadFileTest(ClientInit):
    file_name = 'file.png'

    def _create_image(self):
        return SimpleUploadedFile(self.file_name, 'file_content', content_type='image/png')

    def _upload_file(self, kwargs=None):
        today = date.today()
        fields = {'first_name': 'Javier', 'last_name': 'Perini', 'birthday': today}
        a_person = Person.objects.create(**fields)
        params = kwargs or {}
        image = self._create_image()
        params.update({'file': image})
        url = reverse('update_person', kwargs={'pk': a_person.pk})
        fields.update(params)
        response = self.client.post(url, fields, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        return response, a_person

    def test_response_ok_when_the_file_was_successfully_uploaded(self):
        response, _ = self._upload_file()

        data = response.json()
        self.assertEqual(data['msg'], 'ok')

    def test_redirect_to_home_when_the_file_was_successfully_uploaded(self):
        response, _ = self._upload_file()

        data = response.json()
        self.assertEqual(data['redirect'], reverse('home'))

    def test_upload_file_to_person(self):
        _, person = self._upload_file()
        person.refresh_from_db()
        self.assertEqual(person.images.first().file.name, self.file_name)

    def test_upload_only_file_to_person(self):
        expect_images = PersonImages.objects.count() + 1
        _, person = self._upload_file()
        person.refresh_from_db()
        self.assertEqual(person.images.count(), expect_images)

    def test_update_name_person(self):
        new_name = 'Pedro'

        _, person = self._upload_file({'first_name': new_name})
        person.refresh_from_db()
        self.assertEqual(person.first_name, new_name)

    def tearDown(self):
        "Borro las imagenes despues de los test"
        for p in PersonImages.objects.all():
            p.file.delete()
