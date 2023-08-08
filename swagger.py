import connexion
application = connexion.FlaskApp(__name__)
application.add_api("swagger.yml")
app = application.app
    