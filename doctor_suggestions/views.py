from django.db.models import Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from accounts import custom_permission
# Create your views here.
from doctor_suggestions.models import DoctorHealthSuggestion
from doctor_suggestions.serializers import DoctorHealthSuggestionViewSetSerializer


class DoctorHealthSuggestionByDoctorViewSet(viewsets.ModelViewSet):
    queryset = DoctorHealthSuggestion.objects.all()
    serializer_class = DoctorHealthSuggestionViewSetSerializer
    permission_classes = [custom_permission.IsDoctor]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering = '-id'

    def get_queryset(self):
        return DoctorHealthSuggestion.objects.filter(created_doctor_id=self.request.user.id, is_disable=False,)

    def perform_destroy(self, instance):
        # for disable deletions
        # if u want to delete a suggestion request. update a is disable flag
        pass


class DoctorHealthSuggestionForPatientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DoctorHealthSuggestion.objects.all()
    serializer_class = DoctorHealthSuggestionViewSetSerializer
    permission_classes = [custom_permission.IsPatient]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering = '-id'

    def get_queryset(self):
        return DoctorHealthSuggestion.objects.filter(suggestion_patient_id=self.request.user.id, is_disable=False)
