from . import db
import datetime

""" 
This is highly subject to change.
"""

class Calendar(db.Model):
    __tablename__ = 'calendar'
    id = db.Column(db.String(100), primary_key=True) # This is the primary key
    date = db.Column(db.String(100), nullable=False) # YYYY-MM-DD
    time = db.Column(db.String(100), nullable=False) # HH:MM AM/PM
    name = db.Column(db.String(100), nullable=False) # Name of the event
    # This is a helper method to convert the model to a dictionary
    # Refer to json_format_for_frontend.md
    def to_dict(self):
        return {
            self.date: [
                {
                    'name': self.name,
                    'time': self.time
                }
            ]
        }


class Participant(db.Model):
    __tablename__ = 'participant'
    id = db.Column(db.String(100), primary_key=True)
    calendar_id = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def get_actors(self, calendar_id):
        participant = self.query.filter(self.calendar_id == calendar_id).all()

        list_of_participants = []
        for p in participant:
            list_of_participants.append(p.email)
        return list_of_participants

    def get_ids(self, email):
        participant = self.query.filter(self.email == email).all()

        list_of_ids = []
        for p in participant:
            list_of_ids.append(p.calendar_id)
        return list_of_ids