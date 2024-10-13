from flask import Blueprint, jsonify, request, send_file
from ics import Calendar as cal, Event
import os
from datetime import datetime
from app.models import db
from app.models.tables import Calendar, Active, User
from uuid import uuid4 as uuid

api = Blueprint('api', __name__)

### HEALTH ENDPOINT #########################
@api.route('/health')
def health():
    return jsonify({
            "healthy":True
        }), 200

### CALENDAR ENDPOINTS #######################
# Helper function to save the calendar to the .ics file
def save_calendar(calendar, filename):
    directory = os.path.dirname(filename)

    if directory and not os.path.exists(directory):
        os.makedirs(os.path.dirname(filename
                                    ))
    with open(filename, 'w') as f:
        f.writelines(str(calendar))

# Helper function to find an event by its UID
def find_event_by_uid(calendar, uid):
    for event in calendar.events:
        if event.uid == uid:
            return event
    return None

def get_calendar(nfc):
    filename = f'data/{nfc}.ics'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            calendar = cal(f.read())
    else:
        calendar = cal()
    return calendar

# Get all events
# might be not needed any more
@api.route('/events/<nfc>', methods=['GET'])
def get_events(nfc):
    calendar = get_calendar(nfc)
    events = [{
        'uid': event.uid,
        'name': event.name,
        'begin': event.begin.strftime('%Y-%m-%d %H:%M:%S'),
        'end': event.end.strftime('%Y-%m-%d %H:%M:%S'),
        'description': event.description,
        'location': event.location
    } for event in calendar.events]
    
    return jsonify(events), 200



@api.route('/events/<nfc>', methods=['POST'])
def add_event(nfc):
    calendar = get_calendar(nfc)
    new_event = request.json
    ics_event = Event()
    ics_event.name = new_event['name']
    ics_event.begin = datetime.strptime(new_event['begin'], '%Y-%m-%d %H:%M:%S')
    ics_event.end = datetime.strptime(new_event['end'], '%Y-%m-%d %H:%M:%S')
    ics_event.description = new_event.get('description', '')
    ics_event.location = new_event.get('location', '')

    # Set visibility
    visibility = new_event.get('visibility', 'PUBLIC').upper()
    if visibility not in ['PUBLIC', 'PRIVATE', 'CONFIDENTIAL']:
        # In your post you can set the visibility to PUBLIC, PRIVATE, or CONFIDENTIAL i.e. {'visibility': 'PRIVATE'}
        return jsonify({'error': 'Invalid visibility'}), 400
    ics_event.classification = visibility


    ics_event.uid = f'{ics_event.begin.strftime("%Y%m%d%H%M%S")}-{ics_event.name}'

    calendar.events.add(ics_event)
    save_calendar(calendar, f'data/{nfc}.ics')
    
    return jsonify({'message': 'Event added successfully', 'uid': ics_event.uid}), 201

@api.route('/events/<nfc>/<uid>', methods=['PUT'])
def update_event(nfc, uid):
    calendar = get_calendar(nfc)
    ics_event = find_event_by_uid(uid)
    if not ics_event:
        return jsonify({'error': 'Event not found'}), 404
    
    updated_event = request.json
    ics_event.name = updated_event.get('name', ics_event.name)
    ics_event.begin = datetime.strptime(updated_event['begin'], '%Y-%m-%d %H:%M:%S') if 'begin' in updated_event else ics_event.begin
    ics_event.end = datetime.strptime(updated_event['end'], '%Y-%m-%d %H:%M:%S') if 'end' in updated_event else ics_event.end
    ics_event.description = updated_event.get('description', ics_event.description)
    ics_event.location = updated_event.get('location', ics_event.location)
    save_calendar(calendar, f'data/{nfc}.ics')
    
    return jsonify({'message': 'Event updated successfully'}), 200

@api.route('/events/<nfc>/<uid>', methods=['DELETE'])
def delete_event(nfc, uid):
    calendar = get_calendar(nfc)
    event = find_event_by_uid(calendar, uid)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    calendar.events.remove(event)
    save_calendar(calendar, f'data/{nfc}.ics')
    
    return jsonify({'message': 'Event deleted successfully'}), 200

@api.route('/events/upload/<nfc>', methods=['POST'])
def upload_calendar(nfc):
    file = request.files['file']
    file.save(f'data/{nfc}.ics')
    return jsonify({'message': 'Calendar uploaded successfully'}), 201

### USER ENDPOINTS ##########################

@api.route('/users/<nfc>', methods=['GET'])
def get_user(nfc):
    user = User.query.filter_by(nfcID=nfc).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'userID': user.userID,
        'nfcID': user.nfcID,
        'name': user.name,
        'colour': user.colour
    }), 200

@api.route('/users/all', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([{
        'userID': user.userID,
        'nfcID': user.nfcID,
        'name': user.name,
        'colour': user.colour
    } for user in users]), 200

@api.route('/users', methods=['POST'])
def add_user():
    new_user = request.json
    user_exists = User.query.filter_by(nfcID=new_user['nfcID']).first()
    if user_exists:
        return jsonify({'error': 'User already exists'}), 400
    user = User(userID=str(uuid()), nfcID=new_user['nfcID'], name=new_user['name'], colour=new_user['colour'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User added successfully', 'userID': user.userID}), 201

@api.route('/users/<nfc>', methods=['PUT'])
def update_user(nfc):
    user = User.query.filter_by(nfcID=nfc).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    updated_user = request.json
    user.name = updated_user.get('name', user.name)
    db.session.commit()
    
    return jsonify({'message': 'User updated successfully'}), 200

@api.route('/users/<nfc>', methods=['DELETE'])
def delete_user(nfc):
    user = User.query.filter_by(nfcID=nfc).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'}), 200

@api.route('/active', methods=['GET'])
def get_active():
    for active in Active.query.all():
        if active.isOn:
            return jsonify({'isOn': True}), 200
        
    return jsonify({'isOn': False}), 200

@api.route('/active/<nfc>', methods=['GET'])
def set_active(nfc):
    # Search for user first
    user = User.query.filter_by(nfcID=nfc).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if user isOn = True, set to False, otherwise set to True
    active = Active.query.filter_by(userID=user.userID).first()
    if active:
        active.isOn = not active.isOn
        active.updated = datetime.now()
        db.session.commit()
    else:
        active = Active(userID=user.userID, nfcID=user.nfcID, updated=datetime.now(), isOn=True)
        db.session.add(active)
    db.session.commit()
    for active in Active.query.all():
        if active.isOn:
            return jsonify({'message': 'Active status updated successfully', 'isOn': True}), 200
    return jsonify({'message': 'Active status updated successfully', 'isOn': False}), 200

# ICS ENDPOINTS ##############################

# This is unused, for testing single user
@api.route('/events/<nfc>/ics', methods=['GET'])
def convert_ics_to_events(nfc):
    user = User.query.filter_by(nfcID=nfc).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    calendar = get_calendar(nfc)

    events = []
    # Loop through the events in the calendar
    for event in calendar.events:
        events.append({
            'user': user.name,   # Assuming 'user' is defined somewhere in the scope
            'color': user.colour, # Assuming 'user' is defined somewhere in the scope
            'id': event.uid if event.uid else nfc,  # Use NFC as fallback for ID
            'title': event.name if event.name else "No Title",
            'start': event.begin.strftime('%Y-%m-%d %H:%M:%S'),
            'end': event.end.strftime('%Y-%m-%d %H:%M:%S'),
            'summary': event.description if event.description else "No Summary",
            'location': event.location if event.location else "No Location",
        })

    return jsonify(events), 200

@api.route('/events/ics/all', methods=['GET'])
def convert_ics_to_events_all():
    users = User.query.all()
    active = Active.query.filter_by(isOn=True).all()
    userIsActive = []
    for act in active:
        userIsActive.append(act.userID)
    events = []
    for user in users:
        if user.userID not in userIsActive:
            continue
        calendar = get_calendar(user.nfcID)
        for event in calendar.events:
            if not event.classification or event.classification.upper() == 'PUBLIC':
                events.append({
                    'user': user.name,
                    'color': user.colour,
                    'id': event.uid if event.uid else user.nfcID,
                    'title': event.name if event.name else "No Title",
                    'start': event.begin.strftime('%Y-%m-%d %H:%M:%S'),
                    'end': event.end.strftime('%Y-%m-%d %H:%M:%S'),
                    'summary': event.description if event.description else "No Summary",
                    'location': event.location if event.location else "No Location",
                })
    return jsonify(events), 200