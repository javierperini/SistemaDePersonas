from django import forms
from django.utils import timezone
from sistemaDePersonasApp.models import Person


class PersonForm(forms.ModelForm):
    birthday = forms.DateField(initial=timezone.now().date(),
                               label='Desde',
                               widget=forms.widgets.DateInput(attrs={'class': 'datepicker form-control'}))

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'birthday')
        widgets = {'first_name': forms.TextInput(attrs={'size': 25, 'class': 'form-control',
                                                        'placeholder': 'Ingresa nombre', 'required': True}),
                   'last_name': forms.TextInput(attrs={'size': 25, 'class': 'form-control', 'required': True,
                                                        'placeholder': 'Ingresa apellido'}),}


