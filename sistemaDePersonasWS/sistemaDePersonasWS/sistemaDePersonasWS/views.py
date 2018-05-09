from django.views.generic import TemplateView, CreateView
from sistemaDePersonasApp.models import Person
from sistemaDePersonasWS.forms import PersonForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['persons'] = Person.objects.all()
        return context


class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm


def upload_file(self, pk):
    if self.is_ajax:
        person = get_object_or_404(Person, pk=pk)
        file = self.FILES.get('file')
        person.file = file
        person.save()
        return JsonResponse({'msg': "ok"})
    else:
        return HttpResponseForbidden()