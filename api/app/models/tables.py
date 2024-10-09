from . import db
import datetime


class Calendar(db.Model):
    __tablename__ = 'calendar'
    nfcID = db.Column(db.String(255), primary_key=True)
    filepath = db.Column(db.String(255), nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    userID = db.Column(db.String(255), primary_key=True)
    nfcID = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    colour = db.Column(db.String(255), nullable=False)

class Active(db.Model):
    __tablename__ = 'active'
    userID = db.Column(db.String(255), primary_key=True)
    nfcID = db.Column(db.String(255), nullable=False)
    updated = db.Column(db.DateTime(), nullable=False)
    isOn = db.Column(db.Boolean(), nullable=False)