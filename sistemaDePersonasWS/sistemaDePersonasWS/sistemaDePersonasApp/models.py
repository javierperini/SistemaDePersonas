from __future__ import unicode_literals

from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    birthday = models.DateField()

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    @property
    def has_images(self):
        self.images.exists()


class PersonImages(models.Model):
    file = models.ImageField()
    owner = models.ForeignKey(Person, verbose_name=u'propietario de la imagen', related_name='images')

    def __unicode__(self):
        return u"%s" % self.file.name
