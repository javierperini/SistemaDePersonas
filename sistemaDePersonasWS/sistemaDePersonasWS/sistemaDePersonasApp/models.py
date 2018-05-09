from __future__ import unicode_literals

from django.db import models
from django import forms


class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    birthday = models.DateField()
    file = forms.FileField()

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)
