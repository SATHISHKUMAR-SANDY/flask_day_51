from flask import Flask, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Course, Enrollment
from forms import RegisterForm, LoginForm, EnrollmentForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists.', 'danger')
        else:
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Login successful!', 'info')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = EnrollmentForm()
    form.course.choices = [(c.id, c.name) for c in Course.query.all()]

    if form.validate_on_submit():
        existing = Enrollment.query.filter_by(user_id=current_user.id, course_id=form.course.data).first()
        if existing:
            flash('Already enrolled in this course.', 'warning')
        else:
            enrollment = Enrollment(user_id=current_user.id, course_id=form.course.data)
            db.session.add(enrollment)
            db.session.commit()
            flash('Enrolled successfully!', 'success')
    return render_template('dashboard.html', form=form)

@app.route('/enrollments')
@login_required
def enrollments():
    enrolled_courses = Enrollment.query.filter_by(user_id=current_user.id).all()
    return render_template('enrollments.html', enrollments=enrolled_courses)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Add default courses only once
        if not Course.query.first():
            db.session.add_all([
                Course(name="Python Basics"),
                Course(name="Flask Web Dev"),
                Course(name="SQL for Beginners"),
            ])
            db.session.commit()
    app.run(debug=True)
