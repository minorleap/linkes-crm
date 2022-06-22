from django.db import models
from django.urls import reverse
from client.models import Client
import datetime


class GroupType(models.Model):
    name = models.CharField(max_length=80)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('foodservice:group_type_detail',
                        args=[self.pk])

    def get_edit_url(self):
        return reverse('foodservice:edit_group_type', args=[self.pk])


class Group(models.Model):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=80)
    group_type = models.ForeignKey(GroupType, on_delete=models.PROTECT, related_name='groups')
    capacity = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('foodservice:group_detail',
                        args=[self.pk])

    def get_edit_url(self):
        return reverse('foodservice:edit_group', args=[self.pk])

    def get_places_booked(self):
        return len(self.bookings.filter(active=True))

    def get_remaining_capacity(self):
        return self.capacity - self.get_places_booked()


class GroupSession(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField()
    time = models.TimeField()
    attenders = models.ManyToManyField(Client, related_name='attended_foodservice_sessions', blank=True)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return self.group.group_type.name + ' (' + str(self.date) + ')'

    def get_absolute_url(self):
        return reverse('foodservice:group_session_detail',
                        args=[self.pk])

    def get_attendance(self):
        return len(self.attenders.all())


class GroupBooking(models.Model):
    group = models.ForeignKey(Group, on_delete=models.PROTECT, related_name='bookings')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='foodservice_bookings')
    active = models.BooleanField(default=True)
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
        ordering = ('-active','client__first_name',)    

    def __str__(self):
        return self.group.group_type.name + ' - ' + self.client.first_name + ' ' + self.client.last_name

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
