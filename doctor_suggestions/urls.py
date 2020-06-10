from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from doctor_suggestions.views import DoctorHealthSuggestionByDoctorViewSet, DoctorHealthSuggestionForPatientViewSet

router = DefaultRouter()
router.register('doctor/suggestion-by-doctor', DoctorHealthSuggestionByDoctorViewSet)
router.register('doctor/suggestion-to-patient', DoctorHealthSuggestionForPatientViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
