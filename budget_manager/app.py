from flask import Flask, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Expense
from forms import RegisterForm, LoginForm, ExpenseForm, LimitForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
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
            flash(f"Welcome, {current_user.username}!")
            return redirect(url_for('dashboard'))
        flash("Invalid credentials.")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    expense_form = ExpenseForm()
    limit_form = LimitForm()

    if limit_form.validate_on_submit():
        session['monthly_limit'] = limit_form.limit.data
        flash(f"Monthly limit set to {limit_form.limit.data}")
        return redirect(url_for('dashboard'))

    if expense_form.validate_on_submit():
        expense = Expense(category=expense_form.category.data,
                          amount=expense_form.amount.data,
                          user_id=current_user.id)
        db.session.add(expense)
        db.session.commit()

        total = sum(exp.amount for exp in Expense.query.filter_by(user_id=current_user.id).all())
        limit = session.get('monthly_limit', 0)
        if limit and total > limit:
            flash("⚠️ Warning: You have exceeded your monthly spending limit!")

        flash("Expense added!")
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html',
                           expense_form=expense_form,
                           limit_form=limit_form,
                           limit=session.get('monthly_limit', 0))

@app.route('/summary')
@login_required
def summary():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    total = sum(e.amount for e in expenses)
    return render_template('summary.html', expenses=expenses, total=total)
