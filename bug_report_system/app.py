from flask import Flask, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, Bug
from forms import RegisterForm, LoginForm, BugForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bugs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful.")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"Welcome back, {current_user.username}!")
            return redirect(url_for('dashboard'))
        flash("Invalid login.")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_bugs = Bug.query.filter_by(user_id=current_user.id).all()
    last_title = session.get('last_bug_title', 'N/A')
    return render_template('dashboard.html', bugs=user_bugs, last_title=last_title)

@app.route('/submit-bug', methods=['GET', 'POST'])
@login_required
def submit_bug():
    form = BugForm()
    if form.validate_on_submit():
        bug = Bug(title=form.title.data, description=form.description.data, user_id=current_user.id)
        db.session.add(bug)
        db.session.commit()
        session['last_bug_title'] = form.title.data
        flash("Bug submitted successfully.")
        return redirect(url_for('dashboard'))
    return render_template('submit_bug.html', form=form)
