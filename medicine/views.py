from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import viewsets, filters, status, serializers
from rest_condition import Or
from rest_framework.views import APIView

from accounts import custom_permission
from medicine.models import TreatmentHistory, TreatmentMedicine
from medicine.serializers import TreatmentHistorySerializer


class TreatmentHistoryViewSet(viewsets.ModelViewSet):
    queryset = TreatmentHistory.objects.all()
    serializer_class = TreatmentHistorySerializer
    permission_classes = [Or(custom_permission.IsPatient, custom_permission.IsDoctor, custom_permission.IsMedical)]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering = '-id'

    def get_queryset(self):
        user_id = self.request.user.id
        user_group = list(self.request.user.groups.values_list('name', flat=True))
        if "Patient" in user_group:
            return TreatmentHistory.objects.filter(patient_id=user_id)
        if 'Doctor' in user_group:
            return TreatmentHistory.objects.filter(doctor_id=user_id)
        if 'Medical' in user_group:
            prescription_no = self.request.query_params.get('prescription_no', None)
            if prescription_no is None:
                raise serializers.ValidationError('Prescription No is required')
            else:
                return TreatmentHistory.objects.filter(prescription_no=prescription_no)

        raise serializers.ValidationError("You don't Have a permission")


class UpdateTablet(APIView):
    permission_classes = [custom_permission.IsMedical]

    def post(self, request):
        data = request.data
        print(data)
        medicine = TreatmentMedicine.objects.get(pk=data['id'])
        if medicine.purchased_tablets == medicine.total_tablets:
            return Response(data='already all tablet Purchased', status=status.HTTP_404_NOT_FOUND)
        if medicine.remaining_tablets < int(data['update_tablet']):
            return Response(data='Your asking more tablet. your remaining tablet is ' + medicine.remaining_tablets,
                            status=status.HTTP_404_NOT_FOUND)
        else:
            medicine.purchased_tablets = medicine.purchased_tablets + int(data['update_tablet'])
            medicine.remaining_tablets = medicine.total_tablets - medicine.purchased_tablets
            medicine.save()

            return Response('successfully updated', status=status.HTTP_200_OK)


        return []

