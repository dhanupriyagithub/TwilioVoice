from django.db import models

class CallRecord(models.Model):
    phone_number = models.CharField(max_length=20)
    question1 = models.CharField(max_length=255)
    question2 = models.CharField(max_length=255)
    question3 = models.CharField(max_length=255)
    call_time = models.TimeField()
    recording_url = models.CharField(max_length=255)

    def __str__(self):
        return f"Call Record for {self.phone_number} at {self.call_time}"

    class Meta:
        db_table='myphone'
 

    

    








