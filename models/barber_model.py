from extensions import db


class Barber(db.Model):
    """Barber model for managing barber profiles."""
    
    __tablename__ = 'barbers'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Personal information
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(150))
    experience_years = db.Column(db.Integer, default=1)
    bio = db.Column(db.Text)
    
    # Avatar
    avatar_initials = db.Column(db.String(3))
    
    # Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relationships
    appointments = db.relationship('Appointment', backref='barber', lazy='dynamic')

    def __repr__(self):
        return f'<Barber {self.name}>'
    
    def get_initials(self):
        """Generate initials from name if not set."""
        if not self.avatar_initials:
            self.avatar_initials = ''.join([w[0].upper() for w in self.name.split()[:2]])
        return self.avatar_initials
    
    def to_dict(self):
        """Convert barber to dictionary for API responses."""
        return {
            'id': self.id,
            'name': self.name,
            'specialty': self.specialty,
            'experience_years': self.experience_years,
            'bio': self.bio,
            'avatar_initials': self.avatar_initials or self.get_initials(),
            'is_active': self.is_active,
            'appointments_count': self.appointments.count() if self.appointments else 0
        }


def seed_barbers():
    """Seed database with default barbers if empty."""
    from extensions import db
    
    if Barber.query.count() == 0:
        barbers = [
            Barber(
                name='Sebastián Mora',
                specialty='Fades & Diseños',
                experience_years=8,
                bio='Maestro del fade perfecto. Especialista en diseños geométricos y líneas precisas.',
                avatar_initials='SM'
            ),
            Barber(
                name='Diego Valles',
                specialty='Barba & Afeitado Clásico',
                experience_years=12,
                bio='Experto en el arte del afeitado tradicional. Rituales de barba que transforman.',
                avatar_initials='DV'
            ),
            Barber(
                name='Andrés Reyes',
                specialty='Cortes Premium & Textura',
                experience_years=6,
                bio='Especialista en texturas y cortes modernos. Transforma tu imagen con estilo.',
                avatar_initials='AR'
            ),
            Barber(
                name='Camilo Ortiz',
                specialty='Coloración & Tratamientos',
                experience_years=9,
                bio='Artista del color masculino. Tratamientos capilares de alto rendimiento.',
                avatar_initials='CO'
            ),
        ]
        db.session.add_all(barbers)
        db.session.commit()
