from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import Config
from forms import LoginForm, RegisterForm, JournalForm
from models import db, User, Journal
from datetime import datetime

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
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            session['login_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists.', 'warning')
        else:
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = JournalForm()
    if form.validate_on_submit():
        entry = Journal(content=form.content.data, owner=current_user)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('dashboard'))

    entries = Journal.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', form=form, entries=entries, login_time=session.get('login_time'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    journal = Journal.query.get_or_404(id)
    if journal.owner != current_user:
        flash('Not authorized!', 'danger')
        return redirect(url_for('dashboard'))

    form = JournalForm(obj=journal)
    if form.validate_on_submit():
        journal.content = form.content.data
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('edit.html', form=form)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    journal = Journal.query.get_or_404(id)
    if journal.owner == current_user:
        db.session.delete(journal)
        db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
