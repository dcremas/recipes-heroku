from datetime import datetime
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Authors(UserMixin, db.Model):

    __tablename__ = "authors"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    password_hashed = db.Column(db.String(128), default='')
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    recipes = db.relationship(
        'Recipes',
        backref='author',
        cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"Username: {self.username}, Email: {self.email}"

    def set_password(self, password):
        self.password_hashed = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hashed, password)


class Recipes(UserMixin, db.Model):

    __tablename__ = "recipes"
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    category = db.Column(db.String(25), nullable=False)
    title = db.Column(db.String(25), nullable=False)
    prep_time = db.Column(db.String)
    cooking_time = db.Column(db.String)
    yield_amount = db.Column(db.String)
    ingredients = db.Column(db.String)
    instructions = db.Column(db.String)
    tips = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Category: {self.category}, Title: {self.title}"


##with app.app_context():
##    db.drop_all()       
##    db.create_all()
