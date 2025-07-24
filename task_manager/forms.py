from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=1, max=8)
    ])
    confirm = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')
    ])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[DataRequired()])
    completed = BooleanField('Completed')
    submit = SubmitField('Save Task')
