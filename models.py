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
    username = db.Column(db.String(80), unique = False, nullable = False)
    number_of_posts = db.Column(db.String(80), unique = False, nullable = True)
    number_of_adores = db.Column(db.String(80), unique = False, nullable = True)
    number_of_besties = db.Column(db.String(80), unique = False, nullable = True)
    profile_description = db.Column(db.String(80), unique = False, nullable = True)
    
    
    
    
    def __repr__(self):
        return '<User %r>' % self.email