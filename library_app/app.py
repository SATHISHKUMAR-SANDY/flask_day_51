from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Book, BorrowedBook
from forms import LoginForm

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
    # Add default admin user if not exists
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
    # Add some books if none
    if not Book.query.first():
        books = ['Harry Potter', 'The Hobbit', '1984', 'To Kill a Mockingbird']
        for title in books:
            db.session.add(Book(title=title))
        db.session.commit()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            session['borrowed'] = []  # Reset session borrow list
            flash('Logged in successfully!', 'success')
            return redirect(url_for('books'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash("You've been logged out.", 'info')
    return redirect(url_for('login'))

@app.route('/books')
@login_required
def books():
    all_books = Book.query.all()
    return render_template('books.html', books=all_books)

@app.route('/borrow/<int:book_id>')
@login_required
def borrow(book_id):
    book = Book.query.get_or_404(book_id)
    borrowed = BorrowedBook(user_id=current_user.id, book_id=book.id)
    db.session.add(borrowed)
    db.session.commit()

    # Track recently borrowed in session
    if 'borrowed' not in session:
        session['borrowed'] = []
    session['borrowed'].append(book.title)
    flash(f"You borrowed: {book.title}", 'success')
    return redirect(url_for('books'))

@app.route('/recent')
@login_required
def recent():
    recent_books = session.get('borrowed', [])
    return render_template('recent.html', books=recent_books)

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash("Admins only!", 'danger')
        return redirect(url_for('books'))
    records = BorrowedBook.query.all()
    return render_template('admin.html', records=records)
    
if __name__ == '__main__':
    app.run(debug=True)
