from flask import Flask, request, jsonify, send_file
from ics import Calendar, Event
from datetime import datetime
import os

app = Flask(__name__)

# sample in-memory data
events = []
calendar = Calendar()

filename = 'calendar.ics'
organizer = 'megan.roxburgh' # TODO: link to current user logged in on app/NFC id number

@app.route('/events', methods=['GET'])
def get_events():
    return jsonify(events), 200

@app.route('/events', methods=['POST'])
def create_event():
    new_event = request.json
    ics_event = Event()
    ics_event.name = new_event['name']
    ics_event.begin = new_event['start']
    ics_event.end = new_event['end']
    ics_event.description = new_event.get('description', '')
    ics_event.location = new_event.get('location', '')
    ics_event.organizer = organizer

    calendar.events.add(ics_event)

    with open(filename, 'w') as f:
        f.writelines(calendar)

    return jsonify(new_event), 201

@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    updated_event = request.json
    events[event_id] = updated_event

    calendar_event = list(calendar.events)[event_id]
    calendar_event.name = updated_event['name']
    calendar_event.begin = updated_event['start']
    calendar_event.end = updated_event['end']
    calendar_event.description = updated_event.get('description', '')
    calendar_event.location = updated_event.get('location', '')
    calendar_event.organizer = organizer
    calendar_event.attendees = updated_event.get('attendees', [])

    with open(filename, 'w') as f:
        f.writelines(calendar)

    return jsonify(updated_event), 200

@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    events.pop(event_id)

    event_to_remove = list(calendar.events)[event_id]
    calendar.events.remove(event_to_remove)

    with open(filename, 'w') as f:
        f.writelines(calendar)

    return jsonify({'message': 'Event deleted'}), 204

@app.route('/events/download', methods=['GET'])
def download_calendar():
    if os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({'error': 'Calendar not found'}), 404

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