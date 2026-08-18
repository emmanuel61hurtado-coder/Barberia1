from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from extensions import db
from models import Barber, Service, Appointment, Review
from datetime import datetime, date
from config import Config
import json

client_bp = Blueprint('client', __name__)

@client_bp.route('/')
def index():
    """Landing page with barbers, services, and reviews."""
    barbers = Barber.query.filter_by(is_active=True).all()
    services = Service.query.filter_by(is_active=True).all()
    reviews = Review.query.filter_by(is_active=True).order_by(Review.id).all()
    today = date.today().isoformat()
    
    return render_template(
        'client/index.html',
        barbers=barbers,
        services=services,
        reviews=reviews,
        today=today
    )

@client_bp.route('/reservar', methods=['GET', 'POST'])
def book():
    """Multi-step booking form for appointments."""
    barbers = Barber.query.filter_by(is_active=True).all()
    services = Service.query.filter_by(is_active=True).all()
    today = date.today().isoformat()
    
    # Prepare data for JavaScript
    services_dict = {s.id: {'name': s.name, 'price': s.get_formatted_price()} for s in services}
    barbers_dict = {b.id: {'name': b.name} for b in barbers}

    if request.method == 'POST':
        # Process form submission
        appointment = _process_booking_form(request.form)
        
        if isinstance(appointment, tuple):  # Error case
            errors, appointment_data = appointment
            for error in errors:
                flash(error, 'error')
            return render_template(
                'client/book.html',
                barbers=barbers,
                services=services,
                now=today,
                services_json=json.dumps(services_dict),
                barbers_json=json.dumps(barbers_dict)
            )
        
        # Success case
        flash('¡Reserva realizada con éxito! Te contactaremos para confirmar.', 'success')
        return redirect(url_for('client.confirmation', appointment_id=appointment.id))

    return render_template(
        'client/book.html',
        barbers=barbers,
        services=services,
        now=today,
        services_json=json.dumps(services_dict),
        barbers_json=json.dumps(barbers_dict)
    )


def _process_booking_form(form_data):
    """Process and validate booking form data."""
    from utils import validate_phone_number, validate_email
    
    client_name = form_data.get('client_name', '').strip()
    client_phone = form_data.get('client_phone', '').strip()
    client_email = form_data.get('client_email', '').strip()
    barber_id = form_data.get('barber_id')
    service_id = form_data.get('service_id')
    appointment_date_str = form_data.get('appointment_date')
    appointment_time = form_data.get('appointment_time')
    notes = form_data.get('notes', '').strip()

    errors = []
    
    # Validation
    if not client_name:
        errors.append('El nombre es requerido.')
    if not client_phone:
        errors.append('El teléfono es requerido.')
    elif not validate_phone_number(client_phone):
        errors.append('El formato del teléfono no es válido.')
    if client_email and not validate_email(client_email):
        errors.append('El formato del email no es válido.')
    if not barber_id:
        errors.append('Debes seleccionar un barbero.')
    if not service_id:
        errors.append('Debes seleccionar un servicio.')
    if not appointment_date_str:
        errors.append('La fecha es requerida.')
    if not appointment_time:
        errors.append('La hora es requerida.')

    appointment_date = None
    if not errors:
        try:
            appointment_date = datetime.strptime(appointment_date_str, '%Y-%m-%d').date()
            if appointment_date < date.today():
                errors.append('La fecha no puede ser en el pasado.')
        except ValueError:
            errors.append('Formato de fecha inválido.')

    # Check availability
    if not errors:
        existing = Appointment.query.filter_by(
            barber_id=barber_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).filter(Appointment.status.in_(['pendiente', 'confirmada'])).first()
        
        if existing:
            errors.append('Ese horario ya está ocupado. Por favor elige otro.')

    if errors:
        return (errors, None)

    # Create appointment
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
    
    return appointment

@client_bp.route('/confirmacion/<int:appointment_id>')
def confirmation(appointment_id):
    """Display appointment confirmation page."""
    appointment = Appointment.query.get_or_404(appointment_id)
    return render_template('client/confirmation.html', appointment=appointment)


@client_bp.route('/servicios')
def services():
    """Display services catalog page."""
    services = Service.query.filter_by(is_active=True).all()
    return render_template('client/services.html', services=services)


@client_bp.route('/barberos')
def barbers():
    """Display barbers team page."""
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
        '08:00', '08:30', '09:00', '09:30', '10:00', '10:30',
        '11:00', '11:30', '12:00', '12:30', '13:00', '13:30',
        '14:00', '14:30', '15:00', '15:30', '16:00', '16:30',
        '17:00', '17:30', '18:00', '18:30', '19:00', '19:30',
        '20:00', '20:30', '21:00'
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
