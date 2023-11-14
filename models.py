from flask_login import UserMixin
from json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from app import db

class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(80), unique = False, nullable = False)
    lastname = db.Column(db.String(80), unique = False, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(300), unique = False, nullable = False)
    username = db.Column(db.String(80), unique = False, nullable = False)
    number_of_posts = db.Column(db.String(80), unique = False, nullable = True)
    number_of_adores = db.Column(db.String(80), unique = False, nullable = True)
    number_of_besties = db.Column(db.String(80), unique = False, nullable = True)
    profile_description = db.Column(db.String(80), unique = False, nullable = True)
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'username': self.username,
            'number_of_posts': self.number_of_posts,
            'number_of_adores': self.number_of_adores,
            'number_of_besties': self.number_of_besties,
            'profile_description': self.profile_description,
        }
    
    
    
    def __repr__(self):
        return '<User %r>' % self.email