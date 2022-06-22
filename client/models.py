from django.db import models
from django.utils import timezone
from django.urls import reverse
import datetime

class Client(models.Model):
    HEALTH_STATUS_CHOICES = (
        ('self-isolating', 'Self-isolating'),
        ('vulnerable', 'Vulnerable'),
        ('shielding', 'Shielding'),
    )
    GDPR_CONSENT_CHOICES = (
        ('given_by_client', 'Given by client'),
        ('given_on_behalf', 'Given on behalf of client'),
    )
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('trans', 'Trans'),
        ('non-binary', 'Non-binary'),
        ('prefer not to say', 'Prefer not to say'),
        ('other', 'Other'),
    )
    ETHNICITY_CATEGORY_CHOICES = (
        ('white', 'White'),
        ('asian', 'Asian, Asian-Scottish or Asian-British'),
        ('african', 'African, Caribbean or Black'),
        ('mixed', 'Mixed or Multiple Ethnic Groups'),
        ('other', 'Other Ethnic Group'),
    )
    ETHNICITY_WHITE_CHOICES = (
        ('scottish', 'Scottish'),
        ('english', 'English'),
        ('irish', 'Irish'),
        ('northern_irish', 'Northern Irish'),
        ('british', 'British'),
        ('gypsy_traveller', 'Gypsy/Traveller'),
        ('polish', 'Polish'),
        ('other', 'Other'),
    )
    ETHNICITY_ASIAN_CHOICES = (
        ('pakistani', 'Pakistani, Pakistani Scottish or Pakistani British'),
        ('indian', 'Indian, Indian Scottish or Indian British'),
        ('bangladeshi', 'Bangladeshi, Bangladeshi Scottish or Bangladeshi British'),
        ('chinese', 'Chinese, Chinese Scottish or Chinese British'),
        ('other', 'Other'),
    )
    ETHNICITY_AFRICAN_CHOICES = (
        ('african', 'African, African Scottish or African British'),
        ('caribbean', 'Caribbean, Caribbean Scottish or Caribbean British'),
        ('other', 'Other'),
    )
    ETHNICITY_OTHER_CHOICES = (
        ('arab', 'Arab, Arab Scottish or Arab British'),
        ('other', 'Other'),
    )
    MARRIED_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )
    SEXUAL_ORIENTATION_CHOICES = (
        ('heterosexual', 'Heterosexual'),
        ('lesbian', 'Gay woman/lesbian'),
        ('gay', 'Gay man'),
        ('bisexual', 'Bisexual'),
        ('other', 'Other'),
    )
    RELIGION_CHOICES = (
        ('none', 'No religion or belief'),
        ('buddhist', 'Buddhist'),
        ('christian', 'Christian'),
        ('hindu', 'Hindu'),
        ('jewish', 'Jewish'),
        ('muslim', 'Muslim'),
        ('sikh', 'Sikh'),
        ('other', 'Other'),
    )
    active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, null=True, blank=True)
    address3 = models.CharField(max_length=250, null=True, blank=True)
    town = models.CharField(max_length=250)
    postcode = models.CharField(max_length=8)
    phone = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=250, null=True, blank=True)
    emergency_contact_phone  = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact_relation = models.CharField(max_length=30, null=True, blank=True)
    health_status = models.CharField(choices=HEALTH_STATUS_CHOICES, max_length=20, blank=True, null=True)
    gdpr_consent = models.CharField(choices=GDPR_CONSENT_CHOICES, max_length=15, null=True, blank=True)
    gdpr_consent_giver = models.CharField(max_length=250, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20, null=True, blank=True)
    gender_specify = models.CharField(max_length=30, null=True, blank=True)
    pronouns = models.CharField(max_length=30, null=True, blank=True)
    has_disability = models.BooleanField(default=False)
    physical_impairment = models.BooleanField(default=False)
    sensory_impairment = models.BooleanField(default=False)
    mental_health_condition = models.BooleanField(default=False)
    learning_disability = models.BooleanField(default=False)
    hiv_cancer_ms = models.BooleanField(default=False)
    ethnicity_category = models.CharField(choices=ETHNICITY_CATEGORY_CHOICES, max_length=10, null=True, blank=True)
    ethnicity_white = models.CharField(choices=ETHNICITY_WHITE_CHOICES, max_length=20, null=True, blank=True)
    ethnicity_asian = models.CharField(choices=ETHNICITY_ASIAN_CHOICES, max_length=20, null=True, blank=True)
    ethnicity_african = models.CharField(choices=ETHNICITY_AFRICAN_CHOICES, max_length=20, null=True, blank=True)
    ethnicity_other = models.CharField(choices=ETHNICITY_OTHER_CHOICES, max_length=20, null=True, blank=True)
    ethnicity_specify = models.CharField(max_length=50, null=True, blank=True)
    first_language = models.CharField(max_length=50, null=True, blank=True)
    country_of_origin = models.CharField(max_length=50, null=True, blank=True)
    nationality = models.CharField(max_length=30, null=True, blank=True)
    has_caring_responsibilities = models.BooleanField(default=False)
    primary_carer_child = models.BooleanField(default=False)
    primary_carer_disabled_child = models.BooleanField(default=False)
    primary_carer_disabled_adult = models.BooleanField(default=False)
    primary_carer_older_person = models.BooleanField(default=False)
    secondary_carer = models.BooleanField(default=False)
    married = models.CharField(choices=MARRIED_CHOICES, max_length=3, blank=True, null=True)
    sexual_orientation = models.CharField(choices=SEXUAL_ORIENTATION_CHOICES, max_length=12, null=True, blank=True)
    sexual_orientation_specify = models.CharField(max_length=30, null=True, blank=True)
    religion = models.CharField(choices=RELIGION_CHOICES, max_length=10, null=True, blank=True)
    religion_specify = models.CharField(max_length=30, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('last_name', 'first_name')
        unique_together = ['first_name', 'last_name', 'address1', 'postcode']

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_absolute_url(self):
        return reverse('client:client_detail', args=[self.pk])

    def get_edit_url(self):
        return reverse('client:edit_client', args=[self.pk])

    def get_address(self):
        address = self.address1
        if self.address2:
            address += ', ' + self.address2
        if self.address3:
            address += ', ' + self.address3
        return address

    def get_age(self):
        if self.date_of_birth:
            return str((datetime.date.today() - self.date_of_birth).days // 365)
        else:
            return 'Not given'


class Referral(models.Model):
    REFERRED_TO_CHOICES = (
        ('dmac', 'DMAC'),
        ('nw_food_bank', 'NW Food Bank'),
        ('gha', 'GHA'),
        ('social_work', 'Social Work'),
        ('g13_g14_hub', 'G13/G14 Hub'),
        ('carers_centre', 'Carers Centre'),
        ('wesrec', 'WESREC'),
        ('other', 'Other'),
    )
    referred_to = models.CharField(choices=REFERRED_TO_CHOICES, max_length=30)
    referred_to_other = models.CharField(max_length=50, default=None, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='referrals')
    date = models.DateField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        if self.referred_to == 'other':
            return f'{self.referred_to_other} ({self.date.strftime("%d/%m/%Y")})'
        else:
            return f'{self.get_referred_to_display()} ({self.date.strftime("%d/%m/%Y")})'


class Casenote(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='casenotes')
    date = models.DateField(default=timezone.now)
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'{self.date.strftime("%d/%m/%Y")}: {self.notes}'
