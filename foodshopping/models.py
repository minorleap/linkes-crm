from django.db import models
from django.urls import reverse
from client.models import Client
import datetime


class ShoppingSchedule(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='food_shopping_schedule')
    number_of_adults = models.PositiveSmallIntegerField()
    number_of_children = models.PositiveSmallIntegerField()
    allergies = models.TextField(max_length=100, blank=True, null=True)
    diabetic = models.BooleanField()
    gluten_free = models.BooleanField()
    dairy_free = models.BooleanField()
    vegetarian = models.BooleanField()
    vegan = models.BooleanField()
    halal = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()
    delivery_notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('start_date',)

    def __str__(self):
        return self.client.first_name + ' ' + self.client.last_name + '\'s Schedule'

    def get_absolute_url(self):
        return reverse('foodshopping:shopping_schedule_detail',
                        args=[self.pk])

    def get_edit_url(self):
        return reverse('foodshopping:edit_shopping_schedule', args=[self.pk])

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

    def includes_date(self, date):
        days_since_start_date = (date - self.start_date).days
        whole_weeks_since_start_date = days_since_start_date // 7
        return whole_weeks_since_start_date % 2 == 0



class ShoppingDelivery(models.Model):
    TYPE_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('ad-hoc', 'Ad-hoc'),
    )
    type = models.CharField(max_length=9, choices=TYPE_CHOICES, default='scheduled')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='shopping_deliveries')
    date = models.DateField()
    number_of_adults = models.PositiveSmallIntegerField()
    number_of_children = models.PositiveSmallIntegerField()
    dietary_requirements = models.CharField(max_length=250, null=True, blank=True)
    delivery_notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date',)
        verbose_name_plural = 'Shopping deliveries'
        unique_together = ('client', 'date')

    def __str__(self):
        return 'Shopping Delivery ' + str(self.pk)

    def get_absolute_url(self):
        return reverse('foodshopping:shopping_delivery_detail',
                        args=[self.pk])

    def get_edit_url(self):
        return reverse('foodshopping:edit_shopping_delivery', args=[self.pk])


class ExceptionDate(models.Model):
    date = models.DateField()
    schedule = models.ForeignKey(ShoppingSchedule, on_delete=models.CASCADE, related_name='exception_dates')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return datetime.datetime.strftime(self.date, '%A %d %B %Y')


class MissedDeliveryDate(models.Model):
    date = models.DateField()
    schedule = models.ForeignKey(ShoppingSchedule, on_delete=models.CASCADE, related_name='missed_delivery_dates')
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return datetime.datetime.strftime(self.date, '%A %d %B %Y')
