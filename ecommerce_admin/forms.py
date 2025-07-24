from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ReviewForm(FlaskForm):
    rating = FloatField('Rating (0.0 - 5.0)', validators=[DataRequired(), NumberRange(min=0.0, max=5.0)])
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit Review')
