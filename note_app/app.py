from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Note
from forms import RegisterForm, LoginForm, NoteForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.")
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
            return redirect(url_for('notes'))
        flash("Invalid credentials.")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for('login'))

@app.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data, content=form.content.data, owner=current_user)
        db.session.add(note)
        db.session.commit()
        flash("Note created!")
        return redirect(url_for('notes'))
    user_notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('notes.html', form=form, notes=user_notes)

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.owner != current_user:
        flash("Unauthorized.")
        return redirect(url_for('notes'))
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash("Note updated.")
        return redirect(url_for('notes'))
    return render_template('notes.html', form=form, notes=Note.query.filter_by(user_id=current_user.id).all())

@app.route('/delete/<int:note_id>')
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.owner != current_user:
        flash("Unauthorized.")
        return redirect(url_for('notes'))
    db.session.delete(note)
    db.session.commit()
    flash("Note deleted.")
    return redirect(url_for('notes'))

if __name__ == '__main__':
    app.run(debug=True)
