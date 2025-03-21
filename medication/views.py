#medication/view.py

from django.http import JsonResponse
from .models import Medication
from .serializers import MedicationSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import joblib
import numpy as np
import json

#Load model and matrices
clf = joblib.load(settings.DRUG_INTERACTION_MODEL_PATH)
u = np.load(settings.U_MATRIX_PATH)
vt = np.load(settings.VT_MATRIX_PATH)
drug_index = np.load(settings.DRUG_INDEX_PATH, allow_pickle=True).item()

# Severity Mapping
severity_messages = {
    3: "Major interaction: Serious side effects may occur. Consult a healthcare provider.",
    2: "Moderate interaction: Potential interactions. Seek medical advice if needed.",
    1: "Minor interaction: Minimal effects expected.",
    0: "No known interaction."
}

def preprocess_input(drug_a, drug_b):
    """Prepare input features for prediction."""
    idx1 = drug_index.get(drug_a)
    idx2 = drug_index.get(drug_b)
    if idx1 is None or idx2 is None:
        return None
    return np.concatenate([u[idx1], vt[idx2]])

def predict_interaction(drug_a, drug_b):
    """Predict severity of drug interaction."""
    features = preprocess_input(drug_a, drug_b)
    if features is None:
        return None
    severity_prediction = clf.predict([features])[0]
    return severity_messages.get(severity_prediction, "Unknown interaction level.")

def format_medication_name(name):
    return name.capitalize() if name else name

@swagger_auto_schema(method='post', request_body=MedicationSerializer, responses={201: MedicationSerializer, 400: 'Bad Request'})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_medication(request):
    """Create a new medication and check interactions."""
    data = request.data
    medication_name = format_medication_name(data.get('medication_name'))
    
    if not medication_name:
        return Response({"error": "Medication name is required."}, status=400)

    # Check interactions with existing medications
    interaction_warnings = {}
    existing_medications = Medication.objects.filter(user=request.user)
    for med in existing_medications:
        interaction_result = predict_interaction(med.medication_name, medication_name)
        if interaction_result:
            interaction_warnings[med.medication_name] = interaction_result
    
    # Convert dictionary to JSON
    interaction_warnings_json = json.dumps(interaction_warnings)
    
    # Create medication entry
    medication = Medication.objects.create(
        user=request.user,
        medication_name=medication_name,
        route_of_administration=data.get('route_of_administration', 'oral'),
        dosage_form=data.get('dosage_form', 'tablet'),
        dosage_unit_of_measure=data.get('dosage_unit_of_measure', 'tablet'),
        dosage_quantity_of_units_per_time=data.get('dosage_quantity_of_units_per_time', 1),
        equally_distributed_regimen=True,
        periodic_interval=data.get('periodic_interval', 'daily'),
        dosage_frequency=data.get('dosage_frequency', 1),
        first_time_of_intake=data.get('first_time_of_intake', None),
        stopped_by_datetime=data.get('stopped_by_datetime', None),
        interaction_warning=interaction_warnings,
    )

    serializer = MedicationSerializer(medication)
    return Response(serializer.data, status=201)


@swagger_auto_schema(method='put', request_body=MedicationSerializer, responses={200: MedicationSerializer, 400: 'Bad Request', 404: 'Not Found'})
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_medication(request, primary_key):
    """Update an existing medication."""
    try:
        medication = Medication.objects.get(id=primary_key, user=request.user)
    except Medication.DoesNotExist:
        return Response({"error": "Medication not found."}, status=404)
    
    data = request.data
    medication_name = format_medication_name(data.get('medication_name', medication.medication_name))
    
    # Check interactions with other existing medications
    interaction_warnings = {}
    existing_medications = Medication.objects.filter(user=request.user).exclude(id=primary_key)
    for med in existing_medications:
        interaction_result = predict_interaction(med.medication_name, medication_name)
        if interaction_result:
            interaction_warnings[med.medication_name] = interaction_result
    
    # Update medication fields
    medication.medication_name = medication_name
    medication.route_of_administration = data.get('route_of_administration', medication.route_of_administration)
    medication.dosage_form = data.get('dosage_form', medication.dosage_form)
    medication.dosage_unit_of_measure = data.get('dosage_unit_of_measure', medication.dosage_unit_of_measure)
    medication.dosage_quantity_of_units_per_time = data.get('dosage_quantity_of_units_per_time', medication.dosage_quantity_of_units_per_time)
    medication.equally_distributed_regimen = data.get('equally_distributed_regimen', medication.equally_distributed_regimen)
    medication.periodic_interval = data.get('periodic_interval', medication.periodic_interval)
    medication.dosage_frequency = data.get('dosage_frequency', medication.dosage_frequency)
    medication.first_time_of_intake = data.get('first_time_of_intake', medication.first_time_of_intake)
    medication.stopped_by_datetime = data.get('stopped_by_datetime', medication.stopped_by_datetime)
    medication.interaction_warning = interaction_warnings
    
    medication.save()
    
    serializer = MedicationSerializer(medication)
    return Response(serializer.data, status=200)


@swagger_auto_schema(method='get', responses={200: MedicationSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_medications(request):
    """Retrieve all medications for the authenticated user."""
    medications = Medication.objects.filter(user=request.user)
    serializer = MedicationSerializer(medications, many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='get', responses={200: MedicationSerializer})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_medication(request, primary_key):
    """Retrieve a specific medication."""
    try:
        medication = Medication.objects.get(id=primary_key, user=request.user)
    except Medication.DoesNotExist:
        return Response({"error": "Medication not found."}, status=404)
    
    serializer = MedicationSerializer(medication)
    return Response(serializer.data)

@swagger_auto_schema(method='delete', responses={204: 'No Content'})
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_medication(request, primary_key):
    """Delete a medication."""
    try:
        medication = Medication.objects.get(id=primary_key, user=request.user)
    except Medication.DoesNotExist:
        return Response({"error": "Medication not found."}, status=404)

    medication.delete()
    return Response({"message": "Medication deleted successfully."}, status=204)
