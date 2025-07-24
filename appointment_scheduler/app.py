from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Appointment
from forms import LoginForm, AppointmentForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ✅ FIXED: create tables & admin user inside app context instead of @before_first_request
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You’ve been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", appointments=appointments)

@app.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    form = AppointmentForm()
    if form.validate_on_submit():
        new_appointment = Appointment(
            user_id=current_user.id,
            date=form.date.data,
            time=form.time.data,
            purpose=form.purpose.data
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash("Appointment booked successfully!", "success")
        return redirect(url_for('dashboard'))
    return render_template("book.html", form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    appointment = Appointment.query.get_or_404(id)
    if appointment.user_id != current_user.id:
        flash("Unauthorized access", "danger")
        return redirect(url_for('dashboard'))

    form = AppointmentForm(obj=appointment)
    if form.validate_on_submit():
        appointment.date = form.date.data
        appointment.time = form.time.data
        appointment.purpose = form.purpose.data
        db.session.commit()
        flash("Appointment updated!", "success")
        return redirect(url_for('dashboard'))
    return render_template("edit.html", form=form)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    appointment = Appointment.query.get_or_404(id)
    if appointment.user_id == current_user.id:
        db.session.delete(appointment)
        db.session.commit()
        flash("Appointment canceled.", "info")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
