from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BookForm(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired()])
    pages_read = IntegerField('Pages Read', validators=[DataRequired()])
    submit = SubmitField('Add/Update Book')
