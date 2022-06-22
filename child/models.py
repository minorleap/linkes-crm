from django.db import models
from client.models import Client
from django.utils import timezone
from django.urls import reverse
import datetime

class Child(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('trans', 'Trans'),
        ('non-binary', 'Non-Binary'),
        ('prefer not to say', 'Prefer not to say'),
        ('other', 'Other')
    )
    active = models.BooleanField(default=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='children')
    relationship_to_client = models.CharField(max_length=50)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    date_of_birth = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20, null=True, blank=True)
    pronouns = models.CharField(max_length=30, null=True, blank=True)
    school = models.CharField(max_length=250, null=True, blank=True)
    school_class = models.CharField(max_length=20, null=True, blank=True)
    activities_consent = models.BooleanField(default=False)
    photography_consent = models.BooleanField(default=False)
    is_peer_volunteer = models.BooleanField(default=False)
    has_no_disability = models.BooleanField(default=False)
    has_physical_impairment = models.BooleanField(default=False)
    has_sensory_impairment = models.BooleanField(default=False)
    has_learning_disability = models.BooleanField(default=False)
    has_mental_health_condition = models.BooleanField(default=False)
    has_any_other_disability = models.BooleanField(default=False)
    disability_details = models.TextField(null=True, blank=True)
    languages_spoken = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('last_name', 'first_name')
        unique_together = ['first_name', 'last_name', 'date_of_birth']
        verbose_name_plural = 'children'

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_absolute_url(self):
        return reverse('child:child_detail', args=[self.pk])

    def get_edit_url(self):
        return reverse('child:edit_child', args=[self.pk])

    def get_age(self):
        return (datetime.date.today() - self.date_of_birth).days // 365

    def get_groups(self):
        return ', '.join(set([booking.group.group_type.name for booking in self.bookings.filter(group__active=True)]))
