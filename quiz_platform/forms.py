from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, EqualTo, Length

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=8)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class QuizForm(FlaskForm):
    q1 = RadioField('1. What is the capital of France?',
                    choices=[('A', 'Paris'), ('B', 'Berlin'), ('C', 'London')],
                    validators=[DataRequired()])
    q2 = RadioField('2. 2 + 2 = ?',
                    choices=[('A', '3'), ('B', '4'), ('C', '5')],
                    validators=[DataRequired()])
    q3 = RadioField('3. Flask is a ...',
                    choices=[('A', 'Python Web Framework'), ('B', 'Python Library'), ('C', 'Database')],
                    validators=[DataRequired()])
    submit = SubmitField('Submit Quiz')
