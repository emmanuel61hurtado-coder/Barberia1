from extensions import db

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    duration_minutes = db.Column(db.Integer, default=30)
    category = db.Column(db.String(50), default='corte')
    is_active = db.Column(db.Boolean, default=True)
    appointments = db.relationship('Appointment', backref='service', lazy=True)

    def __repr__(self):
        return f'<Service {self.name}>'

def seed_services():
    from extensions import db
    if Service.query.count() == 0:
        services = [
            Service(name='Corte Premium', description='Corte personalizado con técnica avanzada, lavado y styling final.', price=45000, duration_minutes=45, category='corte'),
            Service(name='Fade & Diseño', description='Fade degradado con líneas y diseños a medida. Arte en tu cabeza.', price=55000, duration_minutes=60, category='corte'),
            Service(name='Barba Clásica', description='Perfilado y recorte de barba con cuchilla, toalla caliente y aceites.', price=35000, duration_minutes=30, category='barba'),
            Service(name='Ritual Completo', description='Corte + Barba + Ritual facial. La experiencia Black Crown definitiva.', price=90000, duration_minutes=90, category='ritual'),
            Service(name='Afeitado Tradicional', description='Afeitado clásico con navaja, espuma artesanal y toallas calientes.', price=40000, duration_minutes=35, category='barba'),
            Service(name='Tratamiento Capilar', description='Hidratación profunda, keratina suave y masaje relajante de cuero cabelludo.', price=65000, duration_minutes=50, category='tratamiento'),
            Service(name='Ritual Facial', description='Limpieza profunda, exfoliación y mascarilla premium para piel masculina.', price=70000, duration_minutes=55, category='tratamiento'),
            Service(name='Kids Cut', description='Corte especial para los más pequeños. Paciencia y resultado garantizado.', price=30000, duration_minutes=30, category='corte'),
        ]
        db.session.add_all(services)
        db.session.commit()
