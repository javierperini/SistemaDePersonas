from django import forms
from django.utils import timezone
from sistemaDePersonasApp.models import Person


class PersonForm(forms.ModelForm):
    date_format = '%d/%m/%Y'
    birthday = forms.DateField(initial=timezone.now().date().strftime(date_format),
                            input_formats=[date_format], label="Desde",
                            widget=forms.widgets.DateInput(format=date_format,
                                                           attrs={'class': 'datepicker form-control'}))

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'birthday')
        widgets = {'first_name': forms.TextInput(attrs={'size': 25, 'class': 'form-control',
                                                        'placeholder': 'Ingresa nombre', 'required': True}),
                   'last_name': forms.TextInput(attrs={'size': 25, 'class': 'form-control', 'required': True,
                                                        'placeholder': 'Ingresa apellido'}),}
