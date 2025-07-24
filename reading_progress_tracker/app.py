from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from forms import LoginForm, BookForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

class BookProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    pages_read = db.Column(db.Integer, nullable=False)

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = BookForm()
    if form.validate_on_submit():
        book = BookProgress.query.filter_by(user_id=current_user.id, title=form.title.data).first()
        if book:
            book.pages_read = form.pages_read.data
        else:
            book = BookProgress(user_id=current_user.id, title=form.title.data, pages_read=form.pages_read.data)
            db.session.add(book)
        db.session.commit()
        flash("Book progress updated!", "success")
        return redirect(url_for('dashboard'))

    books = BookProgress.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', form=form, books=books)

if __name__ == '__main__':
    app.run(debug=True)
