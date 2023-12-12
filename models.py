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
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_description = db.Column(db.String(255), nullable=False)
    post_created_time = db.Column(db.String(255), nullable=False)
    post_images = db.Column(db.JSON, nullable=True)
    post_comments = db.relationship('Comment', backref='post', lazy=True)
    post_likes = db.Column(db.JSON, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)

    def to_dict(self):
        return {
            'post_id': self.id,
            'username': self.username,
            'post_description': self.post_description,
            'post_created_time': self.post_created_time,
            'post_images': self.post_images,
            'post_comments': [comment.to_dict() for comment in self.post_comments],
            'post_likes': self.post_likes,
        }

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(255), nullable=False)
    comment_time = db.Column(db.DateTime, nullable=False)
    comment_user = db.Column(db.String(80), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def to_dict(self):
        return {
            'comment_text': self.comment_text,
            'comment_time': self.comment_time,
            'comment_user': self.comment_user,
        }
    
    def __repr__(self):
        return '<User %r>' % self.email