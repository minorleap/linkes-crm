from django.db import models
from django.urls import reverse
from client.models import Client
import datetime


class PhonecallSchedule(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    WEEKDAY_CHOICES = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
    )
    TIME_OF_DAY_CHOICES = (
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
    )
    FREQUENCY_CHOICES = (
        ('weekly', 'Every Week'),
        ('fortnightly', 'Every 2 Weeks'),
        ('monthly', 'Every 4 Weeks'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    weekday = models.CharField(max_length=9, choices=WEEKDAY_CHOICES)
    time_of_day = models.CharField(max_length=9, choices=TIME_OF_DAY_CHOICES)
    frequency = models.CharField(max_length=11, choices=FREQUENCY_CHOICES)
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='phonecall_schedule')
    start_date = models.DateField()
    end_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('start_date',)

    def __str__(self):
        return self.client.first_name + ' ' + self.client.last_name + '\'s Schedule'

    def get_absolute_url(self):
        return reverse('phonecalls:phonecall_schedule_detail',
                        args=[self.pk])

    def get_edit_url(self):
        return reverse('phonecalls:edit_phonecall_schedule', args=[self.pk])

    def includes_date(self, date):
        correct_weekday = date.strftime('%A').lower() == self.weekday
        days_since_start_date = (date - self.start_date).days
        whole_weeks_since_start_date = days_since_start_date // 7
        if self.frequency == 'weekly':
            return correct_weekday
        if self.frequency == 'fortnightly':
            correct_week = whole_weeks_since_start_date % 2 == 0
            return correct_week and correct_weekday
        if self.frequency == 'monthly':
            correct_week = whole_weeks_since_start_date % 4 == 0
            return correct_week and correct_weekday



class Phonecall(models.Model):
    TYPE_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('ad-hoc', 'Ad-hoc'),
    )
    TIME_OF_DAY_CHOICES = (
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
    )
    type = models.CharField(max_length=9, choices=TYPE_CHOICES, default='scheduled')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='phonecalls')
    date = models.DateField()
    time_of_day = models.CharField(max_length=9, choices=TIME_OF_DAY_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date',)
        verbose_name_plural = 'Phonecalls'
        unique_together = ('client', 'date')

    def __str__(self):
        return 'Phonecall' + str(self.pk)

    def get_absolute_url(self):
        return reverse('phonecalls:phonecall_detail',
                        args=[self.pk])

    def get_edit_url(self):
        return reverse('phonecalls:edit_phonecall', args=[self.pk])


class ExceptionDate(models.Model):
    date = models.DateField()
    schedule = models.ForeignKey(PhonecallSchedule, on_delete=models.CASCADE, related_name='exception_dates')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return datetime.datetime.strftime(self.date, '%A %d %B %Y')


class MissedCallDate(models.Model):
    date = models.DateField()
    schedule = models.ForeignKey(PhonecallSchedule, on_delete=models.CASCADE, related_name='missed_call_dates')
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return datetime.datetime.strftime(self.date, '%A %d %B %Y')


class PhonecallNotes(models.Model):
    date = models.DateField()
    schedule = models.ForeignKey(PhonecallSchedule, on_delete=models.CASCADE, related_name='phonecall_notes')
    notes = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return datetime.datetime.strftime(self.date, '%A %d %B %Y')
