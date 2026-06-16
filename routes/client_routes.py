from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from extensions import db
from models.barber_model import Barber
from models.service_model import Service
from models.appointment_model import Appointment
from models.review_model import Review
from datetime import datetime, date

client_bp = Blueprint('client', __name__)

@client_bp.route('/')
def index():
    barbers = Barber.query.filter_by(is_active=True).all()
    services = Service.query.filter_by(is_active=True).all()
    reviews = Review.query.filter_by(is_active=True).order_by(Review.id).all()
    today = date.today().isoformat()
    return render_template('client/index.html', barbers=barbers, services=services, reviews=reviews, today=today)

@client_bp.route('/reservar', methods=['GET', 'POST'])
def book():
    barbers = Barber.query.filter_by(is_active=True).all()
    services = Service.query.filter_by(is_active=True).all()
    today = date.today().isoformat()

    if request.method == 'POST':
        client_name = request.form.get('client_name', '').strip()
        client_phone = request.form.get('client_phone', '').strip()
        client_email = request.form.get('client_email', '').strip()
        barber_id = request.form.get('barber_id')
        service_id = request.form.get('service_id')
        appointment_date_str = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')
        notes = request.form.get('notes', '').strip()

        errors = []
        if not client_name: errors.append('El nombre es requerido.')
        if not client_phone: errors.append('El teléfono es requerido.')
        if not barber_id: errors.append('Debes seleccionar un barbero.')
        if not service_id: errors.append('Debes seleccionar un servicio.')
        if not appointment_date_str: errors.append('La fecha es requerida.')
        if not appointment_time: errors.append('La hora es requerida.')

        appointment_date = None
        if not errors:
            try:
                appointment_date = datetime.strptime(appointment_date_str, '%Y-%m-%d').date()
                if appointment_date < date.today():
                    errors.append('La fecha no puede ser en el pasado.')
            except ValueError:
                errors.append('Formato de fecha inválido.')

        if not errors:
            existing = Appointment.query.filter_by(
                barber_id=barber_id,
                appointment_date=appointment_date,
                appointment_time=appointment_time
            ).filter(Appointment.status.in_(['pendiente', 'confirmada'])).first()
            if existing:
                errors.append('Ese horario ya está ocupado. Por favor elige otro.')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('client/book.html', barbers=barbers, services=services, now=today)

        appointment = Appointment(
            client_name=client_name,
            client_phone=client_phone,
            client_email=client_email,
            barber_id=int(barber_id),
            service_id=int(service_id),
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            notes=notes,
            status='pendiente'
        )
        db.session.add(appointment)
        db.session.commit()

        flash('¡Reserva realizada con éxito! Te contactaremos para confirmar.', 'success')
        return redirect(url_for('client.confirmation', appointment_id=appointment.id))

    return render_template('client/book.html', barbers=barbers, services=services, now=today)

@client_bp.route('/confirmacion/<int:appointment_id>')
def confirmation(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    return render_template('client/confirmation.html', appointment=appointment)

@client_bp.route('/servicios')
def services():
    services = Service.query.filter_by(is_active=True).all()
    return render_template('client/services.html', services=services)

@client_bp.route('/barberos')
def barbers():
    barbers = Barber.query.filter_by(is_active=True).all()
    return render_template('client/barbers.html', barbers=barbers)

@client_bp.route('/api/horarios-disponibles')
def available_slots():
    barber_id = request.args.get('barber_id')
    date_str = request.args.get('date')
    service_id = request.args.get('service_id')

    if not barber_id or not date_str:
        return jsonify({'slots': []})

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'slots': []})

    # Get service duration
    duration = 30
    if service_id:
        svc = Service.query.get(service_id)
        if svc:
            duration = svc.duration_minutes

    all_slots = [
        '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
        '12:00', '12:30', '14:00', '14:30', '15:00', '15:30',
        '16:00', '16:30', '17:00', '17:30', '18:00', '18:30'
    ]

    booked = Appointment.query.filter_by(
        barber_id=barber_id,
        appointment_date=selected_date
    ).filter(Appointment.status.in_(['pendiente', 'confirmada'])).all()

    booked_times = [a.appointment_time for a in booked]
    available = [s for s in all_slots if s not in booked_times]

    # Count booked for this barber today (for wait time estimation)
    booked_count = len(booked_times)

    barber = Barber.query.get(barber_id)
    barber_name = barber.name if barber else ''

    return jsonify({
        'slots': available,
        'duration': duration,
        'booked_count': booked_count,
        'barber_name': barber_name,
        'total_slots': len(all_slots)
    })
