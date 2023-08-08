from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required
)

# create an instance of LoginManager
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"
# lets create an instane of the database, migration, and bcrypt
db = SQLAlchemy()
migrate =  Migrate()
bcrypt = Bcrypt()

# so we are creating an instance of our flask app in a function to allow for multiple app instance during testing
def createapp():
    app = Flask(__name__, template_folder='templates')
    
    app.secret_key = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:Eronville2023!@localhost/socialmedia"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
    API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

    
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    bcrypt.init_app(app=app)
    # migrate.init_app(app=app)
    login_manager.init_app(app=app)
    swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

    app.register_blueprint(swaggerui_blueprint)

    
    return app

app = createapp()  # Create the Flask app instance

# if __name__ == "__main__":
#     app.run(debug=True)