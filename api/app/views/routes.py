from flask import Blueprint, jsonify, request, send_file
from ics import Calendar as cal, Event
import os
from datetime import datetime
from app.models import db
from app.models.tables import Calendar

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
@api.route('/events/<nfc>', methods=['GET'])
def get_events(nfc):
    calendar = get_calendar(nfc)
    events = [{
        'uid': event.uid,
        'name': event.name,
        'begin': event.begin.strftime('%Y-%m-%d %H:%M:%S'),
        'end': event.end.strftime('%Y-%m-%d %H:%M:%S'),
        'description': event.description
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
    save_calendar(calendar, f'data/{nfc}.ics')
    
    return jsonify({'message': 'Event updated successfully'}), 200

@api.route('/events/<nfc>/<uid>', methods=['DELETE'])
def delete_event(nfc, uid):
    calendar = get_calendar(nfc)
    event = find_event_by_uid(uid)
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