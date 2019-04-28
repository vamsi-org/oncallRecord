from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.


class Pharmacist(models.Model):
    """
    Setting up the model for a pharmacist
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_sterile_trained = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Roster(models.Model):
    """
    I would like the roster to be included here eventually... maybe some day
    """
    pass


class OnCall(models.Model):
    """
    Model used for an on call period
    """
    pharmacist = models.ForeignKey(Pharmacist, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name = 'OnCall'
        unique_together = 'pharmacist','start_date'
        ordering = ['-end_date']

    def __str__(self):
        return f'{self.pharmacist.user.first_name} {self.pharmacist.user.last_name}: {self.start_date:%d/%m/%y} - {self.end_date:%d/%m/%y}'


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
    session = models.ForeignKey(OnCall, on_delete=models.CASCADE)
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

