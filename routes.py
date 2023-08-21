from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    session,
    request
)
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
from models import User
from forms import login_form,register_form

# from connexion import App
#

# from swagger_setup import connexion_app
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#Create the flask app Instance


# SWAGGER_UI_ENABLED = True

# # Create the Connexion app object.
# connexion_app = App(__name__)
# connexion_app.app.logger.setLevel(logging.DEBUG)
# # Add the APIs to the Connexion app object.
# connexion_app.add_api("swagger.yml")

# Create a route that renders the swagger documentation.
# @app.route("/docs")
# def swagger_ui():
#     # from connexion import App  # Import inside the function
#     # connexion_app = App(__name__)
#     # connexion_app.app.logger.setLevel(logging.DEBUG)
#     # connexion_app.add_api("swagger.yml")
#     return connexion_app
#     # return connexion_app.swagger_ui()


# @app.route("/api/docs")
# def swagger_ui():
    # return swagger(app)

#we are setting the session to be permanent and last for one minuite
@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)
# Home Route to render the inex page
@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    """Render the index page."""
    return render_template("index.html",title="Home")

# Login route for user authentication
# @app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
# def login():
#     """Authenticate and log in a user."""
#     form = login_form()

#     if form.validate_on_submit():
#         try:
#             user = User.query.filter_by(email=form.email.data).first()
#             if check_password_hash(user.pwd, form.pwd.data):
#                 login_user(user)
#                 return redirect(url_for('index'))
#             else:
#                 flash("Invalid Username or password!", "danger")
#         except Exception as e:
#             flash(e, "danger")

#     return render_template("auth.html",
#         form=form,
#         text="Login",
#         title="Login",
#         btn_action="Login"
#         )
@app.route("/login", methods=("POST",), strict_slashes=False)
def login():
    """Authenticate and log in a user."""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return {'message': 'Logged in successfully'}, 200
        else:
            return {'message': 'Invalid Username or password'}, 401
    except Exception as e:
        return {'message': str(e)}, 500
    



# @app.route("/register", methods=("POST",), strict_slashes=False)
# def register():
#     """Register a new user."""
#     try:
#         data = request.get_json()
#         email = data.get('email')
#         password = data.get('password')
#         firstname = data.get('firstname')
#         lastname = data.get("lastname")
        
#         newuser = User(
#             firstname=firstname,
#             lastname = lastname,
#             email=email,
#             password=bcrypt.generate_password_hash(password),
#             )

#         db.session.add(newuser)
#         db.session.commit()
#         return {'message': 'Account Successfully created'}, 201

#     except IntegrityError:
#         db.session.rollback()
#         return {'message': 'User already exists!'}, 409
#     except Exception as e:
#         db.session.rollback()
#         return {'message': str(e)}, 500
@app.route("/register", methods=("POST",), strict_slashes=False)
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        firstname = data.get('firstname')
        lastname = data.get("lastname")

        # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {'message': 'User already exists!'}, 409

        # If email doesn't exist, create a new user
        newuser = User(
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=bcrypt.generate_password_hash(password),
        )

        db.session.add(newuser)
        db.session.commit()
        return {'message': 'Account Successfully created'}, 201

    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}, 500

# Logout route to log out the user
@app.route("/logout")
@login_required
def logout():
    """Log out the currently logged-in user."""
    logout_user()
    return redirect(url_for('login'))

# Run the app if this script is executed directly
if __name__ == "__main__":
    # app = createapp()  # Create the app instance here
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))