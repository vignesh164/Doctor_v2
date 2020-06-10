from rest_framework import serializers

from accounts.models import User
from doctor_suggestions.models import DoctorHealthSuggestion


class DoctorHealthSuggestionViewSetSerializer(serializers.ModelSerializer):
    suggestion_patient_name = serializers.CharField(source='suggestion_patient.username', read_only=True)
    created_doctor_name = serializers.CharField(source='created_doctor.name', read_only=True)
    suggestion_patient_id = serializers.ChoiceField(choices=[], write_only=True)

    def __init__(self, *args, **kwargs):
        # this for only display patient user
        self.fields['suggestion_patient_id'].choices = list(User.objects.filter(groups__name='Patient').
                                                            values_list('id', 'username'))
        super(DoctorHealthSuggestionViewSetSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = DoctorHealthSuggestion
        fields = ('suggestion_patient_id', 'suggestion_patient_name', 'created_doctor_name', 'created_datetime',
                  'health_tips', 'is_disable')

    def create(self, validated_data):
        validated_data['created_doctor_id'] = self.context['request'].user.id
        return DoctorHealthSuggestion.objects.create(**validated_data)
