from . import db
from icalendar import Calendar as iCalendar, Event
import datetime
from uuid import uuid4 as uuid

class Calendar(db.Model):
    __tablename__ = 'calendar'
    user_id = db.Column(db.String(255), nullable=False)
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime)
    updated_at = db.Column(db.DateTime, default=datetime.datetime, 
                           onupdate=datetime.datetime)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start': self.start,
            'end': self.end,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def from_ics(ics_content, user_id):
        calendar = iCalendar.from_ical(ics_content)
        events = []

        for component in calendar.walk():
            if component.name == "VEVENT":
                event = Calendar(
                    user_id=user_id,
                    id = str(uuid()),
                    title=str(component.get('summary')),
                    description=str(component.get('description')),
                    start=component.get('dtstart').dt,
                    end=component.get('dtend').dt,
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now()
                )
                events.append(event)
        return events
