from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class AppointmentForm(FlaskForm):
    date = StringField("Date (YYYY-MM-DD)", validators=[DataRequired()])
    time = StringField("Time (e.g., 10:00 AM)", validators=[DataRequired()])
    purpose = StringField("Purpose", validators=[DataRequired(), Length(min=5)])
    submit = SubmitField("Submit")
