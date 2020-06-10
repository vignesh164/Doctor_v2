from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from medicine.views import TreatmentHistoryViewSet, UpdateTablet

router = DefaultRouter()
router.register('medicine/treatment-history', TreatmentHistoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'update-tablet', UpdateTablet.as_view(), name='purchased_tablet_update')
]
