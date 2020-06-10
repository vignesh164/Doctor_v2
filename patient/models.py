from django.db import models
from accounts.models import User

# Create your models here.


class PatientSuggestionsRequest(models.Model):
    medicine_name = models.CharField(max_length=50,)
    disease_info = models.TextField(null=True)
    remarks = models.TextField(null=True)
    created_by = models.ForeignKey(User, related_name='user_patient_request', null=True, on_delete=models.SET_NULL)
    created_datetime = models.DateTimeField(auto_now_add=True)
    is_disable = models.BooleanField(default=False)

    def __str__(self):
        return self.medicine_name

    class Meta:
        db_table = 'patient_suggestions_request'


class PatientSuggestionResponse(models.Model):
    doctor_response = models.TextField()
    suggestion_request = models.ForeignKey(PatientSuggestionsRequest, null=True, on_delete=models.SET_NULL,
                                           related_name='patient_suggestions_history')
    created_by = models.ForeignKey(User, related_name='user_doctor_response', null=True, on_delete=models.SET_NULL)
    created_datetime = models.DateTimeField(auto_now_add=True)
    is_disable = models.BooleanField(default=False)

    class Meta:
        db_table = 'patient_suggestions_response'

