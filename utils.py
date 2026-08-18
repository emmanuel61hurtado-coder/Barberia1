"""Utility functions for the BIGGIE MAKEOVER application."""
from datetime import datetime, date, time, timedelta
from typing import List, Optional


def generate_time_slots(start_time: str, end_time: str, slot_minutes: int = 30) -> List[str]:
    """
    Generate time slots between start and end times.
    
    Args:
        start_time: Start time in 'HH:MM' format
        end_time: End time in 'HH:MM' format
        slot_minutes: Duration of each slot in minutes
        
    Returns:
        List of time strings in 'HH:MM' format
    """
    slots = []
    start = datetime.strptime(start_time, '%H:%M')
    end = datetime.strptime(end_time, '%H:%M')
    
    current = start
    while current < end:
        slots.append(current.strftime('%H:%M'))
        current += timedelta(minutes=slot_minutes)
    
    return slots


def format_currency(amount: float, currency: str = 'COP') -> str:
    """
    Format amount as currency string.
    
    Args:
        amount: Numeric amount to format
        currency: Currency code (default: COP)
        
    Returns:
        Formatted currency string
    """
    if currency == 'COP':
        return f'${amount:,.0f}'
    return f'{currency} {amount:,.2f}'


def format_date(date_obj: date, format_type: str = 'short') -> str:
    """
    Format date object to Spanish locale string.
    
    Args:
        date_obj: Date object to format
        format_type: 'short', 'long', or 'weekday'
        
    Returns:
        Formatted date string in Spanish
    """
    if format_type == 'short':
        return date_obj.strftime('%d/%m/%Y')
    elif format_type == 'long':
        months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        return f"{date_obj.day} de {months[date_obj.month - 1]} de {date_obj.year}"
    elif format_type == 'weekday':
        weekdays = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        return weekdays[date_obj.weekday()]
    return str(date_obj)


def validate_phone_number(phone: str) -> bool:
    """
    Validate Colombian phone number format.
    
    Args:
        phone: Phone number string
        
    Returns:
        True if valid, False otherwise
    """
    # Remove spaces and dashes
    clean_phone = phone.replace(' ', '').replace('-', '')
    
    # Check if it's a valid Colombian number (10 digits starting with 3)
    return len(clean_phone) == 10 and clean_phone.startswith('3')


def validate_email(email: str) -> bool:
    """
    Basic email validation.
    
    Args:
        email: Email string to validate
        
    Returns:
        True if valid format, False otherwise
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def get_available_slots(barber_id: int, appointment_date: date, 
                       booked_appointments: List, all_slots: List[str]) -> List[str]:
    """
    Get available time slots for a barber on a specific date.
    
    Args:
        barber_id: Barber ID
        appointment_date: Date to check
        booked_appointments: List of booked appointments for that date
        all_slots: List of all possible time slots
        
    Returns:
        List of available time slots
    """
    booked_times = [apt.appointment_time for apt in booked_appointments 
                   if apt.barber_id == barber_id and 
                   apt.appointment_date == appointment_date and
                   apt.status in ['pendiente', 'confirmada']]
    
    return [slot for slot in all_slots if slot not in booked_times]


def calculate_duration_slots(service_duration: int, slot_minutes: int = 30) -> int:
    """
    Calculate how many slots a service occupies.
    
    Args:
        service_duration: Service duration in minutes
        slot_minutes: Duration of each slot in minutes
        
    Returns:
        Number of slots needed
    """
    return max(1, (service_duration + slot_minutes - 1) // slot_minutes)