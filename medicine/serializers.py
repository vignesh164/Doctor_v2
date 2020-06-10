from rest_framework import serializers

from medicine.models import TreatmentHistory, TreatmentMedicine, PrescriptionRange


def get_prescription_no():
    prescription = PrescriptionRange.objects.first()
    if prescription:
        if prescription.end == prescription.last:
            raise serializers.ValidationError("Prescription no is empty")
        else:
            prescription.last = prescription.last+1
            prescription.save()
            return prescription.last
    else:
        raise serializers.ValidationError("Prescription range is not available")


class TreatmentMedicineSerializer(serializers.ModelSerializer):
    remaining_tablets = serializers.IntegerField(read_only=True)
    total_tablets = serializers.IntegerField(read_only=True)

    class Meta:
        model = TreatmentMedicine
        fields = ('id', 'medicine_name', 'morning', 'evening', 'night', 'total_tablets', 'purchased_tablets',
                  'remaining_tablets', 'medicine_for_days')


class TreatmentHistorySerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.username', read_only=True)
    patient_name = serializers.CharField(source='patient.username', read_only=True)
    prescription_no = serializers.CharField(read_only=True)
    treatment_medicine = TreatmentMedicineSerializer(many=True, required=True)
    patient_id = serializers.IntegerField(required=True)

    class Meta:
        model = TreatmentHistory
        fields = ('doctor_name', 'patient_name', 'patient_id', 'prescription_no', 'description', 'treatment_date',
                  'treatment_medicine')

    def create(self, validated_data):
        user_group = self.context['request'].user.groups.values_list('name', flat=True)
        if 'Doctor' in user_group:
            validated_data['doctor_id'] = self.context['request'].user.id
            medicines = validated_data.pop('treatment_medicine', None)
            if not medicines:
                raise serializers.ValidationError("Medicines are Required")
            validated_data['prescription_no'] = get_prescription_no()
            history = TreatmentHistory.objects.create(**validated_data)
            for medicine in medicines:
                medicine['treatment_id'] = history.id
                medicine['total_tablets'] = \
                    medicine['remaining_tablets'] = int(medicine['morning'] + medicine['evening'] +
                                                        medicine['night']) * medicine['medicine_for_days']
                TreatmentMedicine.objects.create(**medicine)

            return history
        else:
            raise serializers.ValidationError("You don't have a permission for Create")
