from . import models


from .models import User
from .app import index, register, login, login_twitter, authorize_twitter, manual_verification, logout, dashboard

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        # Import and register route handlers from app.py
        app.add_url_rule('/', 'index', index)
        app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
        app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
        app.add_url_rule('/login-twitter', 'login_twitter', login_twitter)
        app.add_url_rule('/authorize-twitter', 'authorize_twitter', authorize_twitter)
        app.add_url_rule('/auth/twitter/manual', 'manual_verification', manual_verification, methods=['POST'])
        app.add_url_rule('/logout', 'logout', logout)
        app.add_url_rule('/dashboard', 'dashboard', dashboard)

        db.create_all()

    return app


app = create_app()

#
# if __name__ == '__main__':
#     app = create_app()
#     with app.app_context():
#         # Drop all tables and recreate them
#         db.drop_all()
#         db.create_all()
#
#         # Create some user accounts
#         user1 = User(username='user1', password='password1')
#         user2 = User(username='user2', password='password2')
#
#         # Add users to the database
#         db.session.add(user1)
#         db.session.add(user2)
#         db.session.commit()
#
#         app.run(debug=True)
