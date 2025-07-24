from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, JournalForm
from models import db, User, JournalEntry
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
    return redirect(url_for('journal'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists', 'danger')
        else:
            hashed = generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed)
            db.session.add(new_user)
            db.session.commit()
            flash('Registered successfully! Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('journal'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/journal')
@login_required
def journal():
    entries = JournalEntry.query.filter_by(user_id=current_user.id).all()
    return render_template('journal.html', entries=entries)

@app.route('/journal/add', methods=['GET', 'POST'])
@login_required
def add_entry():
    form = JournalForm()
    if form.validate_on_submit():
        entry = JournalEntry(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(entry)
        db.session.commit()
        flash('Journal entry added.', 'success')
        return redirect(url_for('journal'))
    return render_template('journal_form.html', form=form, title="Add Entry")

@app.route('/journal/edit/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    entry = JournalEntry.query.get_or_404(entry_id)
    if entry.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('journal'))
    form = JournalForm(obj=entry)
    if form.validate_on_submit():
        entry.title = form.title.data
        entry.content = form.content.data
        db.session.commit()
        flash('Entry updated.', 'success')
        return redirect(url_for('journal'))
    return render_template('journal_form.html', form=form, title="Edit Entry")

@app.route('/journal/delete/<int:entry_id>')
@login_required
def delete_entry(entry_id):
    entry = JournalEntry.query.get_or_404(entry_id)
    if entry.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('journal'))
    db.session.delete(entry)
    db.session.commit()
    flash('Entry deleted.', 'warning')
    return redirect(url_for('journal'))

if __name__ == '__main__':
    app.run(debug=True)
