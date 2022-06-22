from django.db import models
from django.utils import timezone
from django.urls import reverse
import datetime

class Staff(models.Model):
    active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    address1 = models.CharField(max_length=250, null=True, blank=True)
    address2 = models.CharField(max_length=250, null=True, blank=True)
    address3 = models.CharField(max_length=250, null=True, blank=True)
    town = models.CharField(max_length=250, null=True, blank=True)
    postcode = models.CharField(max_length=8, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('last_name', 'first_name')
        unique_together = ['first_name', 'last_name', 'address1', 'postcode']

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_absolute_url(self):
        return reverse('staff:staff_detail', args=[self.pk])

    def get_edit_url(self):
        return reverse('staff:edit_staff', args=[self.pk])

    def get_address(self):
        address = self.address1
        if self.address2:
            address += ', ' + self.address2
        if self.address3:
            address += ', ' + self.address3
        return address

    def get_roles(self):
        roles = [role.get_name_display() for role in self.roles.all()]
        return ', '.join(roles)


class Role(models.Model):
    NAME_CHOICES = (
        ('volunteer_driver', 'Volunteer Driver'),
        ('volunteer_call_handler', 'Volunteer Call Handler'),
        ('volunteer_other', 'Volunteer Other'),
        ('board_member', 'Board Member'),
        ('session_worker', 'Session Worker'),
        ('play_worker', 'Play Worker'),
    )
    name = models.CharField(choices=NAME_CHOICES, max_length=30)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='roles')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.get_name_display()


class Timesheet(models.Model):
    ROLE_CHOICES = (
        ('volunteer_driver', 'Volunteer Driver'),
        ('volunteer_call_handler', 'Volunteer Call Handler'),
        ('volunteer_other', 'Volunteer Other'),
        ('board_member', 'Board Member'),
        ('session_worker', 'Session Worker'),
        ('play_worker', 'Play Worker'),
    )
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='timesheets')
    week_commencing = models.DateField(blank=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=30)
    monday_hours = models.DecimalField(max_digits=4, decimal_places=2, blank=True)
    tuesday_hours = models.DecimalField(max_digits=4, decimal_places=2, blank=True)
    wednesday_hours = models.DecimalField(max_digits=4, decimal_places=2, blank=True)
    thursday_hours = models.DecimalField(max_digits=4, decimal_places=2, blank=True)
    friday_hours = models.DecimalField(max_digits=4, decimal_places=2, blank=True)
    saturday_hours = models.DecimalField(max_digits=4, decimal_places=2, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('week_commencing',)

    def total_hours(self):
        return sum([self.monday_hours, self.tuesday_hours, self.wednesday_hours, self.thursday_hours, self.friday_hours, self.saturday_hours])

    def __str__(self):
        return str(self.staff) + ' (' + str(self.week_commencing) + '): ' + str(self.total_hours())
