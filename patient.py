


# from flask import Flask, request, jsonify
# from pymongo import MongoClient
# from bson import ObjectId

# app = Flask(__name__)

# # Connect to MongoDB Atlas
# client = MongoClient("mongodb+srv://mongodb:mongodb@cluster0.1lf6i.mongodb.net/")
# db = client["healthcare_db"]  # Name of the database
# patients_collection = db["patients"]  # Name of the collection

# @app.route('/patient', methods=['POST'])
# def create_patient():
#     data = request.get_json()
    
#     # Patient data to be stored in MongoDB
#     patient = {
#         "name": data['name'],
#         "dob": data['dob'],
#         "medical_history": data['medical_history'],
#         "prescriptions": data['prescriptions'],
#         "lab_results": data['lab_results']
#     }

#     # Insert the patient into the database and get the inserted patient ID
#     result = patients_collection.insert_one(patient)
    
#     # Return the patient data with the MongoDB generated ID
#     patient['id'] = str(result.inserted_id)  # Convert ObjectId to string for response
#     return jsonify(patient), 201

# @app.route('/patient/<patient_id>', methods=['GET'])
# def get_patient(patient_id):
#     # Query MongoDB to find the patient by ID
#     patient = patients_collection.find_one({"_id": ObjectId(patient_id)})
    
#     if not patient:
#         return jsonify({'message': 'Patient not found'}), 404

#     # Remove the '_id' field as it's not needed in the response
#     patient['id'] = str(patient['_id'])
#     del patient['_id']
#     return jsonify(patient)

# @app.route('/patient/<patient_id>', methods=['PUT'])
# def update_patient(patient_id):
#     data = request.get_json()

#     # Query MongoDB to find the patient by ID
#     patient = patients_collection.find_one({"_id": ObjectId(patient_id)})
#     if not patient:
#         return jsonify({'message': 'Patient not found'}), 404
    
#     # Update patient details
#     update_data = {
#         "medical_history": data.get('medical_history', patient['medical_history']),
#         "prescriptions": data.get('prescriptions', patient['prescriptions']),
#         "lab_results": data.get('lab_results', patient['lab_results'])
#     }
    
#     # Update the patient record in MongoDB
#     patients_collection.update_one({"_id": ObjectId(patient_id)}, {"$set": update_data})
    
#     # Return the updated patient data
#     patient.update(update_data)
#     patient['id'] = patient_id  # Add patient ID to the response
#     return jsonify(patient)

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)






from flask import Flask, request, jsonify
from uuid import uuid4

app = Flask(__name__)

# In-memory storage for patients
patients = {}

@app.route('/patient', methods=['POST'])
def create_patient():
    data = request.get_json()
    patient_id = str(uuid4())
    patient = {
        'id': patient_id,
        'name': data['name'],
        'dob': data['dob'],
        'medical_history': data['medical_history'],
        'prescriptions': data['prescriptions'],
        'lab_results': data['lab_results']
    }
    patients[patient_id] = patient
    return jsonify(patient), 201

@app.route('/patient/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = patients.get(patient_id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404
    return jsonify(patient)

@app.route('/patient/<patient_id>', methods=['PUT'])
def update_patient(patient_id):
    data = request.get_json()
    patient = patients.get(patient_id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404

    patient['medical_history'] = data.get('medical_history', patient['medical_history'])
    patient['prescriptions'] = data.get('prescriptions', patient['prescriptions'])
    patient['lab_results'] = data.get('lab_results', patient['lab_results'])

    return jsonify(patient)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
