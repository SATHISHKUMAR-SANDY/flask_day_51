from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, Review
from forms import RegisterForm, LoginForm, ReviewForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
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
def home():
    reviews = Review.query.all()
    return render_template('home.html', reviews=reviews)

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
            flash(f"Welcome back, {current_user.username}!")
            return redirect(url_for('home'))
        flash("Invalid credentials.")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for('home'))

@app.route('/add-review', methods=['GET', 'POST'])
@login_required
def add_review():
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(rating=form.rating.data, comment=form.comment.data, user_id=current_user.id)
        db.session.add(review)
        db.session.commit()
        flash("Review submitted!")
        return redirect(url_for('home'))
    return render_template('add_review.html', form=form)
