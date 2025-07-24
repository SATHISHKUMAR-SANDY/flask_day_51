from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Feedback
from forms import LoginForm, FeedbackForm
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.before_request
    def create_admin_if_not_exists():
        # Only run once on first DB access
        if not hasattr(app, 'admin_created'):
            app.admin_created = True
            with app.app_context():
                db.create_all()
                if not User.query.filter_by(username='admin').first():
                    admin = User(username='admin')
                    admin.set_password('admin123')
                    db.session.add(admin)
                    db.session.commit()

    @app.route('/', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash("Login successful!", "success")
                return redirect(url_for('feedback'))
            flash("Invalid credentials", "danger")
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash("Logged out successfully", "info")
        return redirect(url_for('login'))

    @app.route('/feedback', methods=['GET', 'POST'])
    @login_required
    def feedback():
        form = FeedbackForm()
        if form.validate_on_submit():
            fb = Feedback(user_id=current_user.id, message=form.message.data)
            db.session.add(fb)
            db.session.commit()
            flash("Thank you for your feedback!", "success")
            return redirect(url_for('feedback'))
        return render_template('feedback.html', form=form)

    @app.route('/admin')
    @login_required
    def admin():
        if current_user.username != 'admin':
            flash("Access denied!", "danger")
            return redirect(url_for('feedback'))
        feedbacks = Feedback.query.all()
        return render_template('admin.html', feedbacks=feedbacks)

    return app

# Gunicorn entry point
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
