from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, Product
from forms import LoginForm, ProductForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

ADMIN_EMAIL = "admin@example.com"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()
    if not User.query.filter_by(email=ADMIN_EMAIL).first():
        admin = User(email=ADMIN_EMAIL, password=generate_password_hash('admin123'))
        db.session.add(admin)
        db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Logged in successfully.")
            return redirect(url_for('dashboard'))
        flash("Invalid credentials.")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    if current_user.email != ADMIN_EMAIL:
        flash("Access denied.")
        return redirect(url_for('login'))
    products = Product.query.all()
    return render_template('dashboard.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.email != ADMIN_EMAIL:
        flash("Admins only.")
        return redirect(url_for('dashboard'))

    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data
        )
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully.")
        return redirect(url_for('dashboard'))
    return render_template('product_form.html', form=form, action="Add")

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if current_user.email != ADMIN_EMAIL:
        flash("Admins only.")
        return redirect(url_for('dashboard'))

    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.description = form.description.data
        db.session.commit()
        flash("Product updated.")
        return redirect(url_for('dashboard'))

    return render_template('product_form.html', form=form, action="Edit")

@app.route('/delete/<int:product_id>')
@login_required
def delete_product(product_id):
    if current_user.email != ADMIN_EMAIL:
        flash("Admins only.")
        return redirect(url_for('dashboard'))

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted.")
    return redirect(url_for('dashboard'))
