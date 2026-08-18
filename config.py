import os
from datetime import timedelta


class Config:
    """Base configuration class with default values."""
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'blackcrown-secret-2024')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'sqlite:///blackcrown.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Application
    APP_NAME = 'BIGGIE MAKEOVER'
    APP_TAGLINE = 'Resaltate a Ti'
    
    # Contact
    CONTACT_PHONE = '+57 300 000 0000'
    CONTACT_EMAIL = 'hola@blackcrown.co'
    CONTACT_ADDRESS = 'Calle 93 #15-23, Bogotá'
    WHATSAPP_NUMBER = '573000000000'
    
    # Business hours
    BUSINESS_HOURS = 'Lun–Sáb: 9am – 7pm'
    OPENING_TIME = '9:00'
    CLOSING_TIME = '19:00'
    
    # Appointment settings
    APPOINTMENT_SLOT_MINUTES = 30
    APPOINTMENT_SLOTS_START = '08:00'
    APPOINTMENT_SLOTS_END = '21:00'
