from django.db import models
from client.models import Client
from django.utils import timezone
from django.urls import reverse
import datetime

class FoodbankReferral(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='foodbank_referrals')
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date', 'client',)

    def __str__(self):
        return self.client.first_name + ' ' + self.client.last_name + ' - ' + str(self.date)
