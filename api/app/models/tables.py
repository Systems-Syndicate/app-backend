from . import db
from icalendar import Calendar as iCalendar, Event
import datetime
from uuid import uuid4 as uuid

class Calendar(db.Model):
    __tablename__ = 'calendar'
    nfcID = db.Column(db.String(255), primary_key=True)
    filepath = db.Column(db.String(255), nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    userID = db.Column(db.String(255), primary_key=True)
    nfcID = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)