from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class FeedbackForm(FlaskForm):
    message = TextAreaField("Your Feedback", validators=[DataRequired(), Length(min=10)])
    submit = SubmitField("Submit")
