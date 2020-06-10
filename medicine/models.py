from django.db import models

# Create your models here.


class TreatmentHistory(models.Model):
    doctor = models.ForeignKey('accounts.User', related_name='doctor_treatments', null=True, on_delete=models.SET_NULL,)
    patient = models.ForeignKey('accounts.User', related_name='patient_treatments', null=True, on_delete=models.SET_NULL)
    treatment_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True)
    prescription_no = models.CharField(max_length=20)

    class Meta:
        db_table = 'treatment_history'


class TreatmentMedicine(models.Model):
    treatment = models.ForeignKey(TreatmentHistory, related_name='treatment_medicine', null=True, on_delete=models.SET_NULL)
    medicine_name = models.CharField(max_length=50)
    medicine_for_days = models.IntegerField()
    morning = models.BooleanField(default=False)
    evening = models.BooleanField(default=False)
    night = models.BooleanField(default=False)
    total_tablets = models.IntegerField()
    purchased_tablets = models.IntegerField(default=0)
    remaining_tablets = models.IntegerField(default=0)

    class Meta:
        db_table = 'treatment_medicine'


class PrescriptionRange(models.Model):
    start = models.IntegerField()
    end = models.IntegerField()
    last = models.IntegerField()

    class Meta:
        db_table = 'prescription_range'
