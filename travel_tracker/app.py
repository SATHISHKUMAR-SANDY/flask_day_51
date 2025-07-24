from flask import Flask, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, TravelPlan
from forms import RegisterForm, LoginForm, TravelPlanForm, SearchForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already exists", "danger")
        else:
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful!", "success")
            return redirect(url_for('login'))
    return render_template("register.html", form=form)

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
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    plans = TravelPlan.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", plans=plans)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_plan():
    form = TravelPlanForm()
    if form.validate_on_submit():
        plan = TravelPlan(
            place=form.place.data,
            date=form.date.data,
            reason=form.reason.data,
            user_id=current_user.id
        )
        db.session.add(plan)
        db.session.commit()
        flash("Plan added!", "success")
        return redirect(url_for('dashboard'))
    return render_template("add_plan.html", form=form)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        place = form.place.data
        session['last_search'] = place
        results = TravelPlan.query.filter_by(user_id=current_user.id, place=place).all()
    return render_template("search.html", form=form, results=results, last=session.get('last_search'))

# Create tables safely inside app context
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
