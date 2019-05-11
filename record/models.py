from django.db import models
from datetime import datetime
from roster.models import OnCallPeriod
# Create your models here.


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

