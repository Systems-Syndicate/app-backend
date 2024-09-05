from flask import Blueprint, jsonify, request
from app.models import db

api = Blueprint('api', __name__)

### HEALTH ENDPOINT #########################
@api.route('/health')
def health():
    return jsonify({
            "healthy":True
        }), 200

### CALENDAR ENDPOINT #########################
@api.route('/calendar', methods=['GET'])
def get_calendar():
    email = request.args.get('email')
    calendar = db.Calendar()
    return jsonify(calendar.get_all(email)), 200

### UPLOAD ICS ENDPOINT #########################
@api.route('/upload-ics', methods=['POST'])
def upload_ics():
    if 'file' not in request.files:
        return jsonify({
            "error": "No file part"
        }), 400
    
    file = request.files['file']
    print(file.filename)
    if file.filename == '':
        return jsonify({
            "error": "No selected file"
        }), 400
    
    ics_content = file.read().decode('utf-8')
    return jsonify({
        "content": ics_content
    }), 200
