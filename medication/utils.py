# import joblib
# import numpy as np
# import os
# from django.conf import settings

# # Load model and matrices
# BASE_DIR = settings.BASE_DIR
# MODEL_PATH = os.path.join(BASE_DIR, 'drug_interactions/ml_models/')

# clf = joblib.load(os.path.join(MODEL_PATH, 'DDI_rf_model.pkl'))
# u = np.load(os.path.join(MODEL_PATH, 'u_matrix.npy'))
# vt = np.load(os.path.join(MODEL_PATH, 'vt_matrix.npy'))
# drug_index = np.load(os.path.join(MODEL_PATH, 'drug_index.npy'), allow_pickle=True).item()

# # Severity messages mapping
# severity_messages = {
#     3: "Major interaction: These drugs can have serious side effects when taken together. Consult a healthcare provider immediately.",
#     2: "Moderate interaction: These drugs may interact and cause noticeable effects. Use caution and seek medical advice if necessary.",
#     1: "Minor interaction: The interaction between these drugs is minimal, but you may still experience mild effects.",
#     0: "No known interaction: There are no reported interactions between these drugs."
# }

# def preprocess_input(drug_a, drug_b):
#     """Convert drug names to indices and create feature vector."""
#     idx1 = drug_index.get(drug_a)
#     idx2 = drug_index.get(drug_b)

#     if idx1 is None or idx2 is None:
#         return None

#     return np.concatenate([u[idx1], vt[idx2]])

# def predict_interaction(drug_a, drug_b):
#     """Predict drug interaction severity and return a user-friendly message."""
#     features = preprocess_input(drug_a, drug_b)

#     if features is None:
#         return {"error": "Drug not found. Please enter valid generic drug names."}

#     severity_prediction = clf.predict([features])[0]
#     return {"severity": severity_messages.get(severity_prediction, "Unknown interaction level.")}


































# # utils.py
# import joblib
# import numpy as np
# import json
# import os
# from django.conf import settings
# from django.http import JsonResponse
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings

# # Load the model and matrices using the settings
# # Load the model and matrices using the settings
# clf = joblib.load(settings.MODEL_FILE_PATH + '/DDI_rf_model.pkl')
# u = np.load(settings.MODEL_FILE_PATH + '/u_matrix.npy')
# vt = np.load(settings.MODEL_FILE_PATH + '/vt_matrix.npy')
# drug_index = np.load(settings.MODEL_FILE_PATH + '/drug_index.npy', allow_pickle=True).item()



# severity_messages = {
#     3: "Major interaction: These drugs can have serious side effects when taken together. Consult a healthcare provider immediately.",
#     2: "Moderate interaction: These drugs may interact and cause noticeable effects. Use caution and seek medical advice if necessary.",
#     1: "Minor interaction: The interaction between these drugs is minimal, but you may still experience mild effects.",
#     0: "No known interaction: There are no reported interactions between these drugs."
# }

# def check_drug_interaction(drug_a, drug_b):
#     """Check the interaction between two drugs."""
#     # Normalize drug names to lowercase and strip any leading/trailing spaces
#     drug_a = drug_a.strip().lower()
#     drug_b = drug_b.strip().lower()

#     print(f"Searching for: {drug_a} and {drug_b}")  # Debugging log

#     # Convert drug names to indices using `drug_index`
#     idx1 = drug_index.get(drug_a)
#     idx2 = drug_index.get(drug_b)
    
#     if idx1 is None or idx2 is None:
#         print(f"Drug not found: {drug_a} or {drug_b}")  # Debugging log
#         return "Drug not found. Please use generic names."  # Return a custom error message
    
#     # Create feature vector by combining corresponding u and vt vectors
#     features = np.concatenate([u[idx1], vt[idx2]])

#     # Make prediction
#     severity_prediction = clf.predict([features])[0]
#     severity_message = severity_messages.get(severity_prediction, "Unknown interaction level.")
#     return severity_message




