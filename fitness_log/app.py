from flask import Flask, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

from models import db, User, Workout
from forms import RegisterForm, LoginForm, WorkoutForm, UpdateProfileForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed)
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
            flash(f"Welcome, {current_user.username}!")
            return redirect(url_for('dashboard'))
        flash("Invalid credentials.")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = WorkoutForm()
    if form.validate_on_submit():
        session['last_type'] = form.type.data
        workout = Workout(type=form.type.data, value=form.value.data, date=form.date.data, user_id=current_user.id)
        db.session.add(workout)
        db.session.commit()
        flash("Workout logged!")
        return redirect(url_for('dashboard'))
    last_type = session.get('last_type', '')
    form.type.data = last_type
    return render_template('dashboard.html', form=form)

@app.route('/history')
@login_required
def history():
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.date.desc()).all()
    return render_template('history.html', workouts=workouts)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.password, form.current_password.data):
            current_user.password = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash("Password updated successfully.")
            return redirect(url_for('dashboard'))
        else:
            flash("Incorrect current password.")
    return render_template('profile.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
