from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=8)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ExpenseForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add Expense')

class LimitForm(FlaskForm):
    limit = FloatField('Set Monthly Limit', validators=[DataRequired()])
    submit = SubmitField('Save Limit')
