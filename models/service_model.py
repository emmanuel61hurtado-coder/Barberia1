from extensions import db


class Service(db.Model):
    """Service model for managing barber services."""
    
    __tablename__ = 'services'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Service information
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    duration_minutes = db.Column(db.Integer, default=30, nullable=False)
    category = db.Column(db.String(50), default='corte', nullable=False)
    
    # Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relationships
    appointments = db.relationship('Appointment', backref='service', lazy='dynamic')

    def __repr__(self):
        return f'<Service {self.name}>'
    
    def get_formatted_price(self):
        """Return price formatted as currency."""
        return f'${self.price:,.0f}'
    
    def to_dict(self):
        """Convert service to dictionary for API responses."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'formatted_price': self.get_formatted_price(),
            'duration_minutes': self.duration_minutes,
            'category': self.category,
            'is_active': self.is_active,
            'appointments_count': self.appointments.count() if self.appointments else 0
        }


def seed_services():
    """Seed database with default services if empty."""
    from extensions import db
    
    if Service.query.count() == 0:
        services = [
            Service(
                name='Corte Premium',
                description='Corte personalizado con técnica avanzada, lavado y styling final.',
                price=45000,
                duration_minutes=45,
                category='corte'
            ),
            Service(
                name='Fade & Diseño',
                description='Fade degradado con líneas y diseños a medida. Arte en tu cabeza.',
                price=55000,
                duration_minutes=60,
                category='corte'
            ),
            Service(
                name='Barba Clásica',
                description='Perfilado y recorte de barba con cuchilla, toalla caliente y aceites.',
                price=35000,
                duration_minutes=30,
                category='barba'
            ),
            Service(
                name='Ritual Completo',
                description='Corte + Barba + Ritual facial. La experiencia Black Crown definitiva.',
                price=90000,
                duration_minutes=90,
                category='ritual'
            ),
            Service(
                name='Afeitado Tradicional',
                description='Afeitado clásico con navaja, espuma artesanal y toallas calientes.',
                price=40000,
                duration_minutes=35,
                category='barba'
            ),
            Service(
                name='Tratamiento Capilar',
                description='Hidratación profunda, keratina suave y masaje relajante de cuero cabelludo.',
                price=65000,
                duration_minutes=50,
                category='tratamiento'
            ),
            Service(
                name='Ritual Facial',
                description='Limpieza profunda, exfoliación y mascarilla premium para piel masculina.',
                price=70000,
                duration_minutes=55,
                category='tratamiento'
            ),
            Service(
                name='Kids Cut',
                description='Corte especial para los más pequeños. Paciencia y resultado garantizado.',
                price=30000,
                duration_minutes=30,
                category='corte'
            ),
        ]
        db.session.add_all(services)
        db.session.commit()
