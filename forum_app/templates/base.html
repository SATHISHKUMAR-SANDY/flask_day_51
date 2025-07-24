from flask import Flask, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Post, Comment
from forms import RegisterForm, LoginForm, PostForm, CommentForm

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
    return redirect(url_for('forum'))

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
            flash('Registered successfully.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Login successful.', 'info')
            return redirect(url_for('forum'))
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

@app.route('/forum', methods=['GET', 'POST'])
@login_required
def forum():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post created.", "success")
        return redirect(url_for('forum'))

    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('forum.html', form=form, posts=posts)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added.', 'success')
        return redirect(url_for('post_detail', post_id=post.id))
    return render_template('post_detail.html', post=post, form=form)

@app.route('/my-threads')
@login_required
def my_threads():
    posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.timestamp.desc()).all()
    return render_template('my_threads.html', posts=posts)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
