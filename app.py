from flask import Flask, request, jsonify, send_file
from ics import Calendar, Event
from datetime import datetime
import os

app = Flask(__name__)

filename = 'calendar.ics'
if os.path.exists(filename):
    with open(filename, 'r') as f:
        calendar = Calendar(f.read())
else:
    calendar = Calendar()

# Helper function to save the calendar to the .ics file
def save_calendar():
    with open(filename, 'w') as f:
        f.writelines(calendar)

# Helper function to find an event by its UID
def find_event_by_uid(uid):
    for event in calendar.events:
        if event.uid == uid:
            return event
    return None

# Get all events
@app.route('/events', methods=['GET'])
def get_events():
    events = [{
        'uid': event.uid,
        'name': event.name,
        'begin': event.begin.strftime('%Y-%m-%d %H:%M:%S'),
        'end': event.end.strftime('%Y-%m-%d %H:%M:%S'),
        'description': event.description
    } for event in calendar.events]
    
    return jsonify(events)

# Add a new event
@app.route('/events', methods=['POST'])
def add_event():
    new_event = request.json
    ics_event = Event()
    ics_event.name = new_event['name']
    ics_event.begin = datetime.strptime(new_event['begin'], '%Y-%m-%d %H:%M:%S')
    ics_event.end = datetime.strptime(new_event['end'], '%Y-%m-%d %H:%M:%S')
    ics_event.description = new_event.get('description', '')

    ics_event.uid = f'{ics_event.begin.strftime("%Y%m%d%H%M%S")}-{ics_event.name}'

    calendar.events.add(ics_event)
    save_calendar()
    
    return jsonify({'message': 'Event added successfully', 'uid': ics_event.uid})

# Update an existing event
@app.route('/events/<uid>', methods=['PUT'])
def update_event(uid):
    ics_event = find_event_by_uid(uid)
    if not ics_event:
        return jsonify({'error': 'Event not found'}), 404
    
    updated_event = request.json
    ics_event.name = updated_event.get('name', ics_event.name)
    ics_event.begin = datetime.strptime(updated_event['begin'], '%Y-%m-%d %H:%M:%S') if 'begin' in updated_event else ics_event.begin
    ics_event.end = datetime.strptime(updated_event['end'], '%Y-%m-%d %H:%M:%S') if 'end' in updated_event else ics_event.end
    ics_event.description = updated_event.get('description', ics_event.description)
    
    save_calendar()
    
    return jsonify({'message': 'Event updated successfully'})

# Delete an event
@app.route('/events/<uid>', methods=['DELETE'])
def delete_event(uid):
    event = find_event_by_uid(uid)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    calendar.events.remove(event)
    save_calendar()
    
    return jsonify({'message': 'Event deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)


""" 
Full example with sample properties

ics_event = Event()
ics_event.name = 'Team Meeting'
ics_event.begin = '2024-09-17 10:00:00'
ics_event.end = '2024-09-17 11:00:00'
ics_event.description = 'Quarterly project review with team.'
ics_event.location = '123 Main St, Conference Room A'
ics_event.organizer = 'mailto:organizer@example.com'
ics_event.attendees = ['mailto:attendee1@example.com', 'mailto:attendee2@example.com']
ics_event.status = 'CONFIRMED'
ics_event.categories = ['Work', 'Meeting']
ics_event.priority = 1
ics_event.geo = (40.748817, -73.985428)  # Example coordinates
ics_event.url = 'https://example.com/event-details'
ics_event.alarms.append(Alarm(trigger='15 minutes'))  # Reminder 15 minutes before 
"""