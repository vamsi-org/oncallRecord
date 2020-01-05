from django.db import models
from django.core.exceptions import ValidationError
from profile.models import Profile
from datetime import datetime, timedelta

# Create your models here.
"""
Rostered periods (both on call, TDM and extra shifts)
"""

class ExtraShifts(models.Model):
    pass


class OnCallPeriod(models.Model):
    pharmacist = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='periods', limit_choices_to={'role':"Pharmacist"})
    start_date = models.DateField('Start date of on call period.', help_text="The date the on call period starts.")
    end_date = models.DateField('End date of on call period.', help_text="The date the on call period ends.")
    tdm = models.BooleanField('TDM pharmacist', blank=True, help_text="Select this if this is for a pharmacist to "
                                                                      "cover TDM only.")

    class Meta:
        verbose_name = "OnCall Period"
        verbose_name_plural = "OnCall Periods"

    @staticmethod
    def check_overlap(prev_start, prev_end, new_start, new_end, tdm):  # to do : current fires if editing
        overlap = False
        if prev_end == new_start:  # edge case, which is okay
            overlap = False
        elif (prev_start <= new_start < prev_end) or (prev_start <= new_end < prev_end):  # inner cases
            overlap = True
        elif new_start <= prev_start and new_end >= prev_end:
            overlap = True
        return overlap

    def clean(self):
        periods = OnCallPeriod.objects.all()  # todo NOT good practice right here
        for period in periods:
            if self.check_overlap(period.start_date, period.end_date, self.start_date, self.end_date, self.tdm):
                raise ValidationError(
                    f"There is an overlap with another pharmacist on call, "
                    f"{period.pharmacist}: {period.start_date:%d/%m/%y}, {period.end_date:%d/%m/%y}."
                )

    def __str__(self):
        return f'{self.pharmacist.user.first_name}: {self.start_date: %d/%m/%y} - {self.end_date:%d/%m/%y}'


class Call(models.Model):
    TYPES = [
        ("Stock","Stock"),
        ("Drug info","Drug info"),
        ("TDM","TDM"),
        ("Other","Other")
    ]
    CALLERS = [
        ('Nurse','Nurse'),
        ('House Surgeon','House Surgeon'),
        ('Registrar','Registrar'),
        ('Consultant','Consultant'),
        ('Other','Other')
    ]
    HOSPITALS = [
        ('Chch','Christchurch'),
        ('BWD','Burwood'),
        ('HLM','Hillmorton'),
        ('PMH','Princess Margaret'),
        ('Other','Other')
    ]
    session = models.ForeignKey(OnCallPeriod, on_delete=models.CASCADE, related_name='calls')
    time_started = models.DateTimeField(default=datetime.now) # todo validation on this being in session_start - session_end
    call_type = models.CharField(choices=TYPES, max_length=10)
    caller_type = models.CharField(choices=CALLERS, max_length=13)
    caller_hospital = models.CharField(choices=HOSPITALS, max_length=25)
    caller_ward = models.CharField(max_length=10)  # Todo some logic here to set the hospital if the ward is set
    description = models.CharField(max_length=500)
    call_in = models.BooleanField(default=False)
    mileage = models.IntegerField(blank=True, default=0)
    time_ended = models.DateTimeField()
    minutes = models.IntegerField(editable=False)

    class Meta:
        ordering = ['-time_started']

    def save(self, *args, **kwargs):
        diff = self.time_ended - self.time_started  # todo need to add logic here for if it's a call in
        self.minutes = round(diff.total_seconds()/60, 0)
        super(Call, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.time_started:%d/%m} {self.session.pharmacist}: Call type {self.call_type}. Duration: {self.minutes} minutes. Call-in = {self.call_in}'


