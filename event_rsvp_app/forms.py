from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RSVPForm(FlaskForm):
    event_name = StringField("Event Name", validators=[DataRequired(), Length(min=2)])
    attending = BooleanField("Will Attend?")
    submit = SubmitField("RSVP")
