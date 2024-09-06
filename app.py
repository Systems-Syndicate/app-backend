from flask import Flask, request, jsonify

app = Flask(__name__)

# sample in-memory data
events = []

@app.route('/events', methods=['GET'])
def get_events():
    return jsonify(events), 200

@app.route('/events', methods=['ADD'])
def create_event():
    new_event = request.json
    events.append(new_event)
    return jsonify(new_event), 201

@app.route('/events/<int:event_id>', methods=['UPDATE'])
def update_event(event_id):
    updated_event = request.json
    events[event_id] = updated_event
    return jsonify(updated_event), 200

@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    events.pop(event_id)
    return jsonify({'message': 'Event deleted'}), 204

if __name__ == '__main__':
    app.run(debug=True)
