from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from app import db

class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(80), unique = False, nullable = False)
    lastname = db.Column(db.String(80), unique = False, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(300), unique = False, nullable = False)
    
    def __repr__(self):
        return '<User %r>' % self.email