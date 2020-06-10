from rest_framework import serializers
from .models import PatientSuggestionsRequest, PatientSuggestionResponse


class PatientSuggestionsRequestSerializer(serializers.ModelSerializer):
    created_user_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = PatientSuggestionsRequest
        fields = ('medicine_name', 'disease_info', 'remarks', 'created_user_name', 'is_disable')

    def create(self, validated_data):
        validated_data['created_by_id'] = self.context['request'].user.id
        return PatientSuggestionsRequest.objects.create(**validated_data)


class PatientSuggestionsResponseSerializer(serializers.ModelSerializer):
    created_user_name = serializers.CharField(source='created_by.username', read_only=True)
    medicine_name = serializers.CharField(source='suggestion_request.medicine_name', read_only=True)

    class Meta:
        model = PatientSuggestionResponse
        fields = ('doctor_response', 'suggestion_request', 'created_user_name', 'is_disable', 'medicine_name')

    def create(self, validated_data):
        validated_data['created_by_id'] = self.context['request'].user.id
        return PatientSuggestionResponse.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if instance.created_by_id == self.context['request'].user.id:
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError("You can't Modify or delete a Suggestions, Because is not created by You")


class SuggestionHistoryViewSetSerializer(serializers.ModelSerializer):
    created_patient_name = serializers.CharField(source='created_by__user_name', read_only=True)
    doctor_response = serializers.SerializerMethodField()

    def get_doctor_response(self, obj):
        return PatientSuggestionResponse.objects.filter(suggestion_request_id=obj.id, is_disable=False)\
            .values('doctor_response', 'created_by__username', 'created_datetime')

    class Meta:
        model = PatientSuggestionsRequest
        fields = ('medicine_name', 'disease_info', 'remarks', 'created_patient_name', 'created_datetime',
                  'doctor_response')

