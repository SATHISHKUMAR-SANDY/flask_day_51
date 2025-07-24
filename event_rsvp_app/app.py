from flask import Flask, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, RSVP
from forms import LoginForm, RSVPForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()


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
    session.pop('last_rsvp', None)
    flash("You’ve been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    rsvps = RSVP.query.filter_by(user_id=current_user.id).all()
    last_event = session.get('last_rsvp')
    return render_template("dashboard.html", rsvps=rsvps, last_event=last_event)

@app.route('/rsvp', methods=['GET', 'POST'])
@login_required
def rsvp():
    form = RSVPForm()
    if form.validate_on_submit():
        new_rsvp = RSVP(
            user_id=current_user.id,
            event_name=form.event_name.data,
            attending=form.attending.data
        )
        db.session.add(new_rsvp)
        db.session.commit()
        session['last_rsvp'] = form.event_name.data
        flash("Thank you for your RSVP!", "success")
        return redirect(url_for('dashboard'))
    return render_template("rsvp.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)
