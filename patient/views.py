from django.db.models import Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from patient.models import PatientSuggestionsRequest, PatientSuggestionResponse
from patient.serializers import PatientSuggestionsRequestSerializer, PatientSuggestionsResponseSerializer, \
    SuggestionHistoryViewSetSerializer
from accounts import custom_permission
from rest_framework import permissions, filters
# Create your views here.


class PatientSuggestionsRequestViewSet(viewsets.ModelViewSet):
    queryset = PatientSuggestionsRequest.objects.all()
    serializer_class = PatientSuggestionsRequestSerializer
    permission_classes = [custom_permission.IsPatient]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering = '-id'

    def get_queryset(self):
        return PatientSuggestionsRequest.objects.filter(created_by_id=self.request.user.id, is_disable=False)

    def perform_destroy(self, instance):
        # for disable deletions
        # if u want to delete a suggestion request. update a is disable flag
        pass


class PatientSuggestionsResponseViewSet(viewsets.ModelViewSet):
    queryset = PatientSuggestionResponse.objects.all()
    serializer_class = PatientSuggestionsResponseSerializer
    permission_classes = [custom_permission.IsDoctor]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering = '-id'

    def get_queryset(self):
        return PatientSuggestionResponse.objects.filter(created_by_id=self.request.user.id, is_disable=False)

    def perform_destroy(self, instance):
        # for disable deletions
        # if u want to delete a suggestion request. update a is disable flag
        pass


class SuggestionHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PatientSuggestionsRequest.objects.all()
    serializer_class = SuggestionHistoryViewSetSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering = '-id'

    def get_queryset(self):
        response_suggestions = list(PatientSuggestionResponse.objects.filter(created_by_id=self.request.user.id).
                                    values_list('suggestion_request_id', flat=True))
        data = PatientSuggestionsRequest.objects.filter(Q(Q(created_by_id=self.request.user.id)
                                                          | Q(id__in=response_suggestions)),
                                                        is_disable=False)
        return data
