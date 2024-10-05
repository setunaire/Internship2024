from flask import Flask, request, render_template, jsonify, make_response, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import os
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
app.config['SECRET_KEY'] = 'your_secret_key'  # Add a secret key for sessions

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect users to the login page if not logged in

model_name = 'jbochi/madlad400-3b-mt'
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, torch_dtype=torch.float16)
model.to_bettertransformer()

# Load user for flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User model updated with UserMixin for Flask-Login
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}

# Create database tables
with app.app_context():
    db.create_all()

# SIGNUP ROUTE
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("This user already exists. Please log in!")
            return redirect(url_for('login'))
    return render_template('signup.html')

# LOGIN ROUTE
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password_hash, data['password']):
            login_user(user)
            return redirect(url_for('translate'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
    return render_template('login.html')

# LOGOUT ROUTE
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Translation route - only accessible to logged-in users
@app.route('/translate', methods=['GET', 'POST'])
@login_required
def translate():
    if request.method == 'POST':
        input_text = request.form.get("input_text")
        target_language = request.form.get("target_language")
        text = '<2' + target_language + '> ' + input_text
        input_ids = tokenizer(text, return_tensors="pt").input_ids.to(model.device)
        outputs = model.generate(input_ids=input_ids, max_new_tokens=1024)
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return render_template("translate.html", input_text=text, target_language=target_language, translated_text=translated_text)
    return render_template("translate.html")

# Root route redirects to login if not logged in, otherwise to translation service
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('translate'))
    return redirect(url_for('login'))