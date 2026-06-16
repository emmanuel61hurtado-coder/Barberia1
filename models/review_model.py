from extensions import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, default=5)
    comment = db.Column(db.Text, nullable=False)
    service = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def seed_reviews():
    from extensions import db
    if Review.query.count() == 0:
        reviews = [
            Review(client_name='Carlos M.', rating=5, comment='El mejor corte que me han hecho en la vida. Sebastián es un artista, el fade quedó impecable. Ya no voy a ningún otro lado.', service='Fade & Diseño'),
            Review(client_name='Andrés P.', rating=5, comment='Fui por primera vez y quedé sorprendido. El ambiente es increíble, música buena, atención de primera. El ritual completo vale cada peso.', service='Ritual Completo'),
            Review(client_name='Diego R.', rating=5, comment='Diego el barbero me salvó la barba. Tenía un desastre y salí con una barba de revista. Totalmente recomendado.', service='Barba Clásica'),
            Review(client_name='Felipe T.', rating=5, comment='Llevé a mi hijo al Kids Cut y fue genial. El barbero tuvo mucha paciencia y mi hijo salió feliz. Volveremos seguro.', service='Kids Cut'),
            Review(client_name='Mauricio L.', rating=5, comment='La reserva online es muy fácil, en dos minutos tenía mi cita confirmada. El corte premium superó mis expectativas.', service='Corte Premium'),
            Review(client_name='Santiago V.', rating=5, comment='Llevo 6 meses viniendo cada dos semanas. La consistencia en la calidad es lo que más valoro. Camilo es un crack con los tratamientos.', service='Tratamiento Capilar'),
        ]
        db.session.add_all(reviews)
        db.session.commit()
