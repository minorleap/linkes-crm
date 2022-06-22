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
        return reverse('group:group_type_detail',
                        args=[self.pk])

    def get_edit_url(self):
        return reverse('group:edit_group_type', args=[self.pk])


class Group(models.Model):
    active = models.BooleanField(default=True)
    group_type = models.ForeignKey(GroupType, on_delete=models.PROTECT, related_name='groups')
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.PositiveSmallIntegerField()
    creche_capacity = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('start_date',)

    def __str__(self):
        return self.group_type.name + ' (' + str(self.start_date) + ')'

    def get_absolute_url(self):
        return reverse('group:group_detail',
                        args=[self.pk])

    def get_edit_url(self):
        return reverse('group:edit_group', args=[self.pk])

    def get_places_booked(self):
        return len(self.bookings.all())

    def get_creche_places_booked(self):
        return sum([booking.creche_spaces for booking in self.bookings.all()])

    def get_remaining_capacity(self):
        return self.capacity - self.get_places_booked()

    def get_remaining_creche_capacity(self):
        return self.creche_capacity - self.get_creche_places_booked()       


class GroupSession(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField()
    time = models.TimeField()
    attenders = models.ManyToManyField(Client, related_name='attended_sessions', blank=True)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return self.group.group_type.name + ' (' + str(self.date) + ')'

    def get_absolute_url(self):
        return reverse('group:group_session_detail',
                        args=[self.pk])

    def get_attendance(self):
        return len(self.attenders.all())


class GroupBooking(models.Model):
    group = models.ForeignKey(Group, on_delete=models.PROTECT, related_name='bookings')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='bookings')
    creche_spaces = models.PositiveSmallIntegerField(default=0)
    names_of_children = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.group.group_type.name + ' - ' + self.client.first_name + ' ' + self.client.last_name
