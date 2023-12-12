import datetime
from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    session,
    request
)
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import os
import logging
from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError


from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from app import app,db,login_manager,bcrypt
from models import Comment, Post, User
from forms import EditProfileForm, login_form,register_form

# from connexion import App
#

# from swagger_setup import connexion_app
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#Create the flask app Instance

#we are setting the session to be permanent and last for ten minuite
@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)
# Home Route to render the inex page
@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    """Render the index page."""
    return render_template("index.html",title="Home")

@app.route("/login", methods=("POST",))
def login():
    """Authenticate and log in a user."""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            token = create_access_token(identity=user.to_dict())
            return {'message': 'Logged in successfully','token': token}, 200
        else:
            return {'message': 'Invalid Username or password'}, 401
    except Exception as e:
        return {'message': str(e)}, 500
    


@app.route("/register", methods=("POST",))
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        firstname = data.get('firstname')
        lastname = data.get("lastname")
        username = data.get("username")

        # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {'message': 'User already exists!'}, 409

        # If email doesn't exist, create a new user
        newuser = User(
            firstname=firstname,
            lastname=lastname,
            email=email,
            username=username,
            password=bcrypt.generate_password_hash(password),
        )

        db.session.add(newuser)
        db.session.commit()
        return {'message': 'Account Successfully created'}, 201

    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}, 500

@app.route("/profile", methods=("POST",))
@jwt_required()
def profile():
    """Get User Profile"""
    # try:
    #     data = request.get_json()
    #     email = data.get('email')

    #     # Find the user based on the provided email
    #     user = User.query.filter_by(email=email).first()

    #     if user:
    #         user_data = {
    #             'username': user.username,
    #             'number_of_posts': user.number_of_posts,
    #             'number_of_besties': user.number_of_besties,
    #             'number_of_adores': user.number_of_adores,
    #             'profile_description': user.profile_description
    #         }
    #         return user_data, 201
    #     else:
    #         return {'message': 'User not found'}, 404

    # except Exception as e:
    #     return {'message': str(e)}, 500
     # Assuming you have a current_user object from Flask-Login .
    try:
        user_id = get_jwt_identity().get("id")
        user = User.query.get(user_id)

        if user:
            user_data = {
                'username': user.username,
                'number_of_posts': user.number_of_posts,
                'number_of_besties': user.number_of_besties,
                'number_of_adores': user.number_of_adores,
                'profile_description': user.profile_description
            }
            return user_data, 200
        else:
            return {'message': 'User not found'}, 404
    except Exception as e:
            return {'message': str(e)}, 500
    # if current_user.is_authenticated:
    #     user_data = {
    #         'username': current_user.username,  # Replace with the actual attribute name
    #         # 'number_of_posts': len(current_user.number_of_posts),  # Replace with the attribute that holds posts
    #         'number_of_posts': current_user.number_of_posts,  # Replace with the attribute that holds posts
    #         'number_of_adores': current_user.number_of_adores,  # Replace with the actual attribute
    #         'profile_description': current_user.profile_description  # Replace with the actual attribute
    #     }
    #     return user_data, 201, user
    # else:
    #     return {'message': 'User not authenticated'}, 401
@app.route("/editprofile", methods=["POST"])
@jwt_required()
def editprofile():
    try:
        user_id = get_jwt_identity().get("id")
        user = User.query.get(user_id)

        if not user:
            return {"message": "User not found"}, 404

        form = EditProfileForm(request.form)
        data = request.get_json()
        if 'username' not in data or 'bio' not in data:
            return {"message": "Username and bio are required fields"}, 400
        username = data.get('username')
        bio = data.get('bio')
        if user:
            user.username = username
            user.profile_description = bio
            user_data_updated = {
                'username': user.username,
                'profile_description': user.profile_description
            }

            db.session.commit()

            return {"message": "Profile updated successfully", "user":  user_data_updated}, 200
        else:
            return {'message': 'Invalid Username or password'}, 401
            
     
    except Exception as e:
        return {"message": str(e)}, 500
@app.route("/createpost", methods=["POST"])
@jwt_required()
def createpost():
    try:
        user_id = get_jwt_identity().get("id")
        user = User.query.get(user_id)
        
        if not user:
            return {"message": "User not found"}, 404

        data = request.get_json()
        post_description = data.get('post_description')
        post_created_time = datetime.datetime.now()
        post_images = data.get('post_images', [])
        post_comments = data.get('post_comments', [])
        post_likes = data.get('post_likes', [])
        username = user.username

        new_post = Post(
            post_description=post_description,
            post_created_time=post_created_time,
            post_images=post_images,
            post_likes=post_likes,
            user_id=user_id,  # Add user_id to the new_post object
            username  = username
            # author=user,
        )

        db.session.add(new_post)
        db.session.commit()

        # Add comments to the post
        for comment_data in post_comments:
            comment = Comment(
                comment_text=comment_data.get('comment_text'),
                comment_time=datetime.datetime.now(),
                comment_user=comment_data.get('comment_user'),
                post=new_post,
            )
            db.session.add(comment)

        db.session.commit()

        return {"message": "Post created successfully", "post": new_post.to_dict()}, 201

    except Exception as e:
        return {"message": str(e)}, 500
# Logout route to log out the user
@app.route("/logout",methods=("GET", ))
@jwt_required()
def logout():
    """Log out the currently logged-in user."""
    try:
        user_id = get_jwt_identity().get("id")
        user = User.query.get(user_id)

        if user:
             logout_user()
             return {'message': 'You have been logged out sucessfully'}, 201
        else:
            return {'message': 'User not found'}, 404
    except Exception as e:
            return {'message': str(e)}, 500
   
    
    # if current_user.is_authenticated:
       
    # else:
        
    #     return {'message': 'User not authenticated'}, 401
    

# Run the app if this script is executed directly
if __name__ == "__main__":
    # app = createapp()  # Create the app instance here
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))