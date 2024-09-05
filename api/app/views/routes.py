from flask import Blueprint, jsonify, request
from app.models import db
from app.models.tables import Calendar

api = Blueprint('api', __name__)

### HEALTH ENDPOINT #########################
@api.route('/health')
def health():
    return jsonify({
            "healthy":True
        }), 200

@api.route('/calendar/<user>', methods=['GET'])
def get_calendar(user):
    events = Calendar.query.filter_by(user_id=user).all()
    events_data = [event.to_dict() for event in events]
    return jsonify({
        "events": events_data
    }), 200

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
    
    user_id = "placeholder"
    events = Calendar.from_ics(file.read().decode("utf-8"), user_id)

    for event in events:
        db.session.add(event)
    db.session.commit()
    
    events_data = [event.to_dict() for event in events]
    return jsonify({
        "events": events_data
    }), 200
        
