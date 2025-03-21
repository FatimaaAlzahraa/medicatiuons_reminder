#medication/serializers.py
from rest_framework import serializers
from .models import Medication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ReminderTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # because there is a field in the reminder model that link it to the respective user, one can access fields of reminder by going through the keys of dictionary
        token['id'] = user.reminder_user.id
        token['medicine_name'] = user.reminder_user.medicine_name
        token['route_of_administration'] = user.reminder_user.route_of_administration
        token['dosage_form'] = user.reminder_user.dosage_form
        token['dosage_quantity_of_units_per_time'] = user.reminder_user.dosage_quantity_of_units_per_time
        token['periodic_interval'] = user.reminder_user.periodic_interval
        token['dosage_frequency'] = user.reminder_user.dosage_frequency
        token['first_time_of_intake'] = user.reminder_user.first_time_of_intake
        token['stopped_by_datetime'] = user.reminder_user.stopped_by_datetime
        token['interaction_warning'] = user.reminder_user.interaction_warning


class MedicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medication
        fields = [
            'id',
            'medication_name',
            'route_of_administration',
            'dosage_form',
            'dosage_unit_of_measure',
            'dosage_quantity_of_units_per_time',
            'equally_distributed_regimen',
            'periodic_interval',
            'dosage_frequency',
            'first_time_of_intake',
            'stopped_by_datetime',
            'interaction_warning',
        ]

    
    def validate_medication_name(self, value):
        if not value:
            raise serializers.ValidationError("Medication name cannot be empty.")
        return value
    
    def validate_dosage_quantity_of_units_per_time(self, value):
        if value <= 0:
            raise serializers.ValidationError("Dosage quantity must be a positive number.")
        return value

