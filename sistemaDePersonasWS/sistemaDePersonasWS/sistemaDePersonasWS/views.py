from django.views.generic import TemplateView, CreateView, UpdateView
from sistemaDePersonasApp.models import Person, PersonImages
from sistemaDePersonasWS.forms import PersonForm
from django.http import JsonResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib import messages


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['persons'] = Person.objects.all()
        return context


class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
    template_name = "sistemaDePersonasApp/create_person.html"

    def post(self, request, *args, **kwargs):
        response = super(PersonCreateView, self).post(request, *args, **kwargs)
        messages.info(request, 'Se registro la persona correctamente')
        return response


class PersonUpdateView(UpdateView):
    model = Person
    form_class = PersonForm
    template_name = "sistemaDePersonasApp/update_person.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.get_object())
        if request.is_ajax and form.is_valid():
            form.save()
            for img in request.FILES.getlist('file'):
                PersonImages.objects.create(file=img, owner=form.instance)
            return JsonResponse({'msg': "ok", 'redirect': reverse('home')})
        else:
            return HttpResponseForbidden()