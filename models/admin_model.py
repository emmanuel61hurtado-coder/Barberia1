from extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Admin {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

def seed_admin():
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(username='admin', email='admin@blackcrown.com')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
