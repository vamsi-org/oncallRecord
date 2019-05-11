from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.
"""
The idea here is for the roster app to house all the info on users, user groups and when someone is on call

The record should be accessed from here to populate the data
"""


class Pharmacist(models.Model):
    """
    Setting up the model for a pharmacist
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_sterile_trained = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class OnCallPeriod(models.Model):
    pharmacist = models.ForeignKey(Pharmacist, on_delete=models.CASCADE, related_name='periods')
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
        return f'{self.pharmacist}: {self.start_date: %d/%m/%y} - {self.end_date:%d/%m/%y}'

