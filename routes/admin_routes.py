from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import Admin, Barber, Service, Appointment
from datetime import datetime, date

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page."""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Credenciales incorrectas.', 'error')

    return render_template('admin/login.html')


@admin_bp.route('/logout')
@login_required
def logout():
    """Admin logout."""
    logout_user()
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard with statistics and recent appointments."""
    today = date.today()
    
    # Statistics
    total_appointments = Appointment.query.count()
    today_appointments = Appointment.query.filter_by(appointment_date=today).count()
    pending = Appointment.query.filter_by(status='pendiente').count()
    completed = Appointment.query.filter_by(status='completada').count()

    # Recent appointments
    recent_appointments = Appointment.query.order_by(
        Appointment.created_at.desc()
    ).limit(8).all()

    # Today's appointments
    today_list = Appointment.query.filter_by(appointment_date=today).order_by(
        Appointment.appointment_time
    ).all()

    # Total revenue from completed appointments
    total_revenue = db.session.query(
        db.func.sum(Service.price)
    ).join(Appointment, Appointment.service_id == Service.id).filter(
        Appointment.status == 'completada'
    ).scalar() or 0

    return render_template(
        'admin/dashboard.html',
        total_appointments=total_appointments,
        today_appointments=today_appointments,
        pending=pending,
        completed=completed,
        recent_appointments=recent_appointments,
        today_list=today_list,
        total_revenue=total_revenue
    )

@admin_bp.route('/citas')
@login_required
def appointments():
    """Appointments management page with filtering."""
    status_filter = request.args.get('status', '')
    date_filter = request.args.get('date', '')

    query = Appointment.query

    if status_filter:
        query = query.filter_by(status=status_filter)
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter_by(appointment_date=filter_date)
        except ValueError:
            pass

    appointments = query.order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time
    ).all()

    return render_template(
        'admin/appointments.html',
        appointments=appointments,
        status_filter=status_filter,
        date_filter=date_filter
    )

@admin_bp.route('/citas/<int:appointment_id>/estado', methods=['POST'])
@login_required
def update_appointment_status(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    new_status = request.form.get('status')
    if new_status in ['pendiente', 'confirmada', 'completada', 'cancelada']:
        appointment.status = new_status
        db.session.commit()
        flash(f'Estado actualizado a: {appointment.status_label()}', 'success')
    return redirect(url_for('admin.appointments'))

@admin_bp.route('/citas/<int:appointment_id>/eliminar', methods=['POST'])
@login_required
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    flash('Cita eliminada.', 'success')
    return redirect(url_for('admin.appointments'))

@admin_bp.route('/barberos')
@login_required
def barbers():
    barbers = Barber.query.all()
    return render_template('admin/barbers.html', barbers=barbers)

@admin_bp.route('/barberos/nuevo', methods=['GET', 'POST'])
@login_required
def new_barber():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        specialty = request.form.get('specialty', '').strip()
        experience = request.form.get('experience_years', 1)
        bio = request.form.get('bio', '').strip()

        if not name:
            flash('El nombre es requerido.', 'error')
            return render_template('admin/barber_form.html', barber=None)

        initials = ''.join([w[0].upper() for w in name.split()[:2]])
        barber = Barber(
            name=name, specialty=specialty,
            experience_years=int(experience), bio=bio,
            avatar_initials=initials
        )
        db.session.add(barber)
        db.session.commit()
        flash('Barbero agregado con éxito.', 'success')
        return redirect(url_for('admin.barbers'))

    return render_template('admin/barber_form.html', barber=None)

@admin_bp.route('/barberos/<int:barber_id>/editar', methods=['GET', 'POST'])
@login_required
def edit_barber(barber_id):
    barber = Barber.query.get_or_404(barber_id)
    if request.method == 'POST':
        barber.name = request.form.get('name', barber.name).strip()
        barber.specialty = request.form.get('specialty', barber.specialty).strip()
        barber.experience_years = int(request.form.get('experience_years', barber.experience_years))
        barber.bio = request.form.get('bio', barber.bio).strip()
        barber.is_active = 'is_active' in request.form
        barber.avatar_initials = ''.join([w[0].upper() for w in barber.name.split()[:2]])
        db.session.commit()
        flash('Barbero actualizado.', 'success')
        return redirect(url_for('admin.barbers'))
    return render_template('admin/barber_form.html', barber=barber)

@admin_bp.route('/servicios')
@login_required
def services():
    services = Service.query.all()
    return render_template('admin/services.html', services=services)

@admin_bp.route('/servicios/nuevo', methods=['GET', 'POST'])
@login_required
def new_service():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', 0)
        duration = request.form.get('duration_minutes', 30)
        category = request.form.get('category', 'corte')

        if not name or not price:
            flash('Nombre y precio son requeridos.', 'error')
            return render_template('admin/service_form.html', service=None)

        service = Service(
            name=name, description=description,
            price=float(price), duration_minutes=int(duration),
            category=category
        )
        db.session.add(service)
        db.session.commit()
        flash('Servicio creado con éxito.', 'success')
        return redirect(url_for('admin.services'))

    return render_template('admin/service_form.html', service=None)

@admin_bp.route('/servicios/<int:service_id>/editar', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)
    if request.method == 'POST':
        service.name = request.form.get('name', service.name).strip()
        service.description = request.form.get('description', service.description).strip()
        service.price = float(request.form.get('price', service.price))
        service.duration_minutes = int(request.form.get('duration_minutes', service.duration_minutes))
        service.category = request.form.get('category', service.category)
        service.is_active = 'is_active' in request.form
        db.session.commit()
        flash('Servicio actualizado.', 'success')
        return redirect(url_for('admin.services'))
    return render_template('admin/service_form.html', service=service)
