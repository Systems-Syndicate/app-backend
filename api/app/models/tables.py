from . import db
import datetime

class Calendar(db.Model):
    __tablename__ = 'calendar'
    user_id = db.Column(db.String(255), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime)
    updated_at = db.Column(db.DateTime, default=datetime.datetime, 
                           onupdate=datetime.datetime)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start': self.start,
            'end': self.end,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def get_all(self, email):
        event = self.query.filter(self.email == email).all()
        list_of_events = []
        for e in event:
            list_of_events.append(e.to_dict())
        return list_of_events
    
    def to_ics(self):
        events = self.get_all()
        ics = ""
        for event in events:
            ics += "BEGIN:VEVENT\n"
            ics += "DTSTART:" + event['start'] + "\n"
            ics += "DTEND:" + event['end'] + "\n"
            ics += "SUMMARY:" + event['title'] + "\n"
            ics += "DESCRIPTION:" + event['description'] + "\n"
            ics += "END:VEVENT\n"
        return ics
    