from extensions import db
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_phone = db.Column(db.String(20), nullable=False)
    client_email = db.Column(db.String(120))
    barber_id = db.Column(db.Integer, db.ForeignKey('barbers.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(10), nullable=False)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='pendiente')  # pendiente, confirmada, completada, cancelada
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Appointment {self.client_name} - {self.appointment_date}>'

    def status_class(self):
        classes = {
            'pendiente': 'status-pending',
            'confirmada': 'status-confirmed',
            'completada': 'status-completed',
            'cancelada': 'status-cancelled'
        }
        return classes.get(self.status, 'status-pending')

    def status_label(self):
        labels = {
            'pendiente': 'Pendiente',
            'confirmada': 'Confirmada',
            'completada': 'Completada',
            'cancelada': 'Cancelada'
        }
        return labels.get(self.status, 'Pendiente')
