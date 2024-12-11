from flask import Flask, render_template
from  config import Config
from extensions import db
from flask_migrate import Migrate
from routes import main , user_bp
from models import User
from models import Category
from models import Comment
from models import Post
from scripts.seed import seed_database
from controllers import user_controllers



# app = Flask(__name__)
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_resources(app)
    register_extensions(app)
    # seed_resources(app)
    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app,db)
# def seed_resources(app):
#     @app.before_request
#     def seed():
#         seed_database()
#         print("Database seeded Successfully")
def register_resources(app):
    app.register_blueprint(main)
    app.register_blueprint(user_bp)

if __name__ == '__main__':
    app = create_app()
    app.run('127.0.0.1', 5000, debug=True)