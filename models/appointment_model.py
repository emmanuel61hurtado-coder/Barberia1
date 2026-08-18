from extensions import db
from datetime import datetime


class Appointment(db.Model):
    """Appointment model for managing client bookings."""
    
    __tablename__ = 'appointments'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Client information
    client_name = db.Column(db.String(100), nullable=False)
    client_phone = db.Column(db.String(20), nullable=False)
    client_email = db.Column(db.String(120))
    
    # Foreign keys
    barber_id = db.Column(db.Integer, db.ForeignKey('barbers.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    
    # Appointment details
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(10), nullable=False)
    notes = db.Column(db.Text)
    
    # Status management
    status = db.Column(db.String(20), default='pendiente', nullable=False)
    # Valid statuses: pendiente, confirmada, completada, cancelada
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships are defined in related models using backref

    def __repr__(self):
        return f'<Appointment {self.client_name} - {self.appointment_date} {self.appointment_time}>'

    def status_class(self):
        """Return CSS class for current status."""
        classes = {
            'pendiente': 'status-pending',
            'confirmada': 'status-confirmed',
            'completada': 'status-completed',
            'cancelada': 'status-cancelled'
        }
        return classes.get(self.status, 'status-pending')

    def status_label(self):
        """Return human-readable status label."""
        labels = {
            'pendiente': 'Pendiente',
            'confirmada': 'Confirmada',
            'completada': 'Completada',
            'cancelada': 'Cancelada'
        }
        return labels.get(self.status, 'Pendiente')
    
    def is_active(self):
        """Check if appointment is still active (not cancelled or completed)."""
        return self.status in ['pendiente', 'confirmada']
    
    def to_dict(self):
        """Convert appointment to dictionary for API responses."""
        return {
            'id': self.id,
            'client_name': self.client_name,
            'client_phone': self.client_phone,
            'client_email': self.client_email,
            'barber_id': self.barber_id,
            'barber_name': self.barber.name if self.barber else None,
            'service_id': self.service_id,
            'service_name': self.service.name if self.service else None,
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'appointment_time': self.appointment_time,
            'notes': self.notes,
            'status': self.status,
            'status_label': self.status_label(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
