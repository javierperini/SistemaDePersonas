from django.views.generic import TemplateView, CreateView
from sistemaDePersonasApp.models import Person
from sistemaDePersonasWS.forms import PersonForm


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['persons'] = Person.objects.all()
        return context


class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
