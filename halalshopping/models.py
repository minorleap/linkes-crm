from django.db import models
from django.urls import reverse
from client.models import Client
import datetime


class ShoppingSchedule(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    TIME_CHOICES = (
        ('13:00', '13:00 - 13:15'),
        ('13:15', '13:15 - 13:30'),
        ('13:30', '13:30 - 13:45'),
        ('13:45', '13:45 - 14:00'),
        ('14:00', '14:00 - 14:15'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    time = models.CharField(max_length=5, choices=TIME_CHOICES)
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='halal_shopping_schedule')
    number_of_adults = models.PositiveSmallIntegerField()
    number_of_children = models.PositiveSmallIntegerField()
    allergies = models.TextField(max_length=100, blank=True, null=True)
    diabetic = models.BooleanField()
    gluten_free = models.BooleanField()
    dairy_free = models.BooleanField()
    vegetarian = models.BooleanField()
    vegan = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('start_date',)

    def __str__(self):
        return self.client.first_name + ' ' + self.client.last_name + '\'s Schedule'

    def get_absolute_url(self):
        return reverse('halalshopping:shopping_schedule_detail',
                        args=[self.pk])

    def get_edit_url(self):
        return reverse('halalshopping:edit_shopping_schedule', args=[self.pk])

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
        if self.allergies:
            dietary_requirements.append('allergic to ' + self.allergies.lower())
        return dietary_requirements


class ShoppingCollection(models.Model):
    TYPE_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('ad-hoc', 'Ad-hoc'),
    )
    TIME_CHOICES = (
        ('13:00', '13:00 - 13:15'),
        ('13:15', '13:15 - 13:30'),
        ('13:30', '13:30 - 13:45'),
        ('13:45', '13:45 - 14:00'),
        ('14:00', '14:00 - 14:15'),
    )
    type = models.CharField(max_length=9, choices=TYPE_CHOICES, default='scheduled')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='shopping_collections')
    date = models.DateField()
    time = models.CharField(max_length=5, choices=TIME_CHOICES)
    number_of_adults = models.PositiveSmallIntegerField()
    number_of_children = models.PositiveSmallIntegerField()
    dietary_requirements = models.CharField(max_length=250, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date',)
        verbose_name_plural = 'Shopping collections'
        unique_together = ('client', 'date')

    def __str__(self):
        return 'Shopping Collection ' + str(self.pk)

    def get_absolute_url(self):
        return reverse('halalshopping:shopping_collection_detail',
                        args=[self.pk])

    def get_edit_url(self):
        return reverse('halalshopping:edit_shopping_collection', args=[self.pk])


class ExceptionDate(models.Model):
    date = models.DateField()
    schedule = models.ForeignKey(ShoppingSchedule, on_delete=models.CASCADE, related_name='exception_dates')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return datetime.datetime.strftime(self.date, '%A %d %B %Y')


class MissedCollectionDate(models.Model):
    date = models.DateField()
    schedule = models.ForeignKey(ShoppingSchedule, on_delete=models.CASCADE, related_name='missed_collection_dates')
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return datetime.datetime.strftime(self.date, '%A %d %B %Y')
