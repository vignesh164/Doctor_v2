from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import PatientSuggestionsRequestViewSet, PatientSuggestionsResponseViewSet, SuggestionHistoryViewSet

router = DefaultRouter()
router.register('patient/suggestion-request', PatientSuggestionsRequestViewSet)
router.register('patient/suggestion-response', PatientSuggestionsResponseViewSet)
router.register('patient/patient-doctor-suggestion-history', SuggestionHistoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
