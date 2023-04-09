from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import User, TwitterAccount
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
import os
import tweepy

# Load environment variables from the .env file
load_dotenv()

CONSUMER_KEY = os.environ.get("TWITTER_API_KEY")
CONSUMER_SECRET = os.environ.get("TWITTER_API_KEY_SECRET")
APP_SECRET_KEY = os.environ.get("APP_SECRET_KEY")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///netporter.db'
app.secret_key = APP_SECRET_KEY

db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize OAuth
oauth = OAuth(app)

# Configure Twitter OAuth
twitter = oauth.register(
    name='twitter',
    client_id=CONSUMER_KEY,
    client_secret=CONSUMER_SECRET,
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    api_base_url='https://api.twitter.com/1.1/',
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username is already taken.', 'danger')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

# Redirect the user to Twitter authorization URL
@app.route('/login-twitter')
def login_twitter():
    redirect_uri = url_for('authorize_twitter', _external=True)
    return twitter.authorize_redirect(redirect_uri)

# Handle the callback from Twitter after user authorization
@app.route('/authorize-twitter')
def authorize_twitter():
    token = twitter.authorize_access_token()
    twitter_account_info = twitter.get('account/verify_credentials.json').json()

    # Save the user's Twitter account information
    save_twitter_account(twitter_account_info, token)

    # Redirect the user to the main page or dashboard
    return redirect(url_for('dashboard'))

# Function to save the user's Twitter account information
def save_twitter_account(twitter_account_info, token):
    # Implement the logic to save the Twitter account information
    # in the database, associated with the current user.
    pass

@app.route('/auth/twitter/manual', methods=['POST'])
def manual_verification():
    # ... handle the manual verification process and obtain the Twitter username
    twitter_username = "example_username"

    # Create and save the new TwitterAccount instance without the access token
    new_twitter_account = TwitterAccount(user_id=current_user.id, twitter_username=twitter_username)
    db.session.add(new_twitter_account)
    db.session.commit()

    # ... other code, such as redirecting the user to the dashboard



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)
