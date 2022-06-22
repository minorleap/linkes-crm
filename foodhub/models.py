from django.db import models
from django.urls import reverse
from client.models import Client
import datetime


class FoodhubCollection(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='foodhub_collections')
    date = models.DateField()
    number_of_adults = models.PositiveSmallIntegerField()
    number_of_children = models.PositiveSmallIntegerField()
    allergies = models.TextField(max_length=100, blank=True, null=True)
    diabetic = models.BooleanField()
    gluten_free = models.BooleanField()
    dairy_free = models.BooleanField()
    vegetarian = models.BooleanField()
    vegan = models.BooleanField()
    halal = models.BooleanField()
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date',)
        verbose_name_plural = 'Food Hub collections'
        unique_together = ('client', 'date')

    def __str__(self):
        return 'Food Hub Collection ' + str(self.pk)

    def get_absolute_url(self):
        return reverse('foodhub:collection_detail',
                        args=[self.pk])

    def get_edit_url(self):
        return reverse('foodhub:edit_collection', args=[self.pk])

    def get_dietary_requirements(self):
        dietary_requirements = []
        if self.diabetic:
            dietary_requirements.append('diabetic')
        if self.gluten_free:
            dietary_requirements.append('gluten-free')
        if self.dairy_free:
            dietary_requirements.append('dairy-free')
        if self.vegetarian:
            dietary_requirements.append('vegetarian')
        if self.vegan:
            dietary_requirements.append('vegan')
        if self.halal:
            dietary_requirements.append('halal')            
        if self.allergies:
            dietary_requirements.append('allergic to ' + self.allergies.lower())
        return dietary_requirements
