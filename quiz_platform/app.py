from flask import Flask, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Book
from forms import LoginForm, BookForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        flash("Invalid credentials", "danger")
    return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout():
    session.pop('last_book', None)
    logout_user()
    flash("You’ve been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    books = Book.query.filter_by(user_id=current_user.id).all()
    last_book = session.get('last_book')
    return render_template("dashboard.html", books=books, last_book=last_book)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BookForm()
    if form.validate_on_submit():
        book = Book.query.filter_by(user_id=current_user.id, title=form.title.data).first()
        if book:
            book.pages_read = form.pages_read.data
        else:
            book = Book(
                title=form.title.data,
                pages_read=form.pages_read.data,
                user_id=current_user.id
            )
            db.session.add(book)
        db.session.commit()
        session['last_book'] = book.title
        flash("Book progress updated!", "success")
        return redirect(url_for('dashboard'))
    return render_template("add_book.html", form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
