from app import createapp, db
from flask_migrate import upgrade, migrate, init, stamp
from models import User

def deploy():
    """Run Deployment tasks here"""
    
    app = createapp()
    with app.app_context():
         init()
        #  stamp()
        #  migrate()
         upgrade()
         db.create_all()

    # Migrate database to the latest version
   

# deploy()
if __name__ == "__main__":
    deploy()