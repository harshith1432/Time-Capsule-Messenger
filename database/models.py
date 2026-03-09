from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    whatsapp_number = db.Column(db.String(20), unique=True, nullable=False)
    otp_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

class Capsule(db.Model):
    __tablename__ = 'capsules'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('capsules', lazy=True))
    message = db.Column(db.Text, nullable=False)
    voice_file = db.Column(db.String(255), nullable=True)
    image_file = db.Column(db.String(255), nullable=True)
    delivery_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending') # pending, delivered, failed
    privacy_type = db.Column(db.String(20), default='private') # private, public
    recipient_number = db.Column(db.String(20), nullable=True) # Send to someone else
    password_hash = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
