from django.views.generic import TemplateView
from sistemaDePersonasApp.models import Person


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['persons'] = Person.objects.all()
        return context
