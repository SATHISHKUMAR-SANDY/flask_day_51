from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, Score
from forms import RegisterForm, LoginForm, QuizForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
            return redirect(url_for('dashboard'))
        flash("Invalid credentials.")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_scores = Score.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', scores=user_scores)

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    form = QuizForm()
    if form.validate_on_submit():
        score = 0
        if form.q1.data == 'A': score += 1
        if form.q2.data == 'B': score += 1
        if form.q3.data == 'A': score += 1
        new_score = Score(score=score, user_id=current_user.id)
        db.session.add(new_score)
        db.session.commit()
        flash(f"Quiz completed. You scored {score}/3.")
        return redirect(url_for('results'))
    return render_template('quiz.html', form=form)

@app.route('/results')
@login_required
def results():
    latest_score = Score.query.filter_by(user_id=current_user.id).order_by(Score.id.desc()).first()
    return render_template('results.html', score=latest_score)

# Create DB tables before first request manually in __main__
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
