from django.db import models

# Create your models here.


class DoctorHealthSuggestion(models.Model):
    suggestion_patient = models.ForeignKey('accounts.User', null=True, on_delete=models.SET_NULL,
                                           related_name='doctor_suggestion_for_me')
    created_doctor = models.ForeignKey('accounts.User', null=True, on_delete=models.SET_NULL,
                                       related_name='doctor_suggestion_by_me')
    created_datetime = models.DateTimeField(auto_now_add=True)
    health_tips = models.TextField()
    is_disable = models.BooleanField(default=False)

    class Meta:
        db_table = 'doctor_health_suggestion'
