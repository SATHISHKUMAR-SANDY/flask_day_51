from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class TravelPlanForm(FlaskForm):
    place = StringField("Place", validators=[DataRequired()])
    date = StringField("Date", validators=[DataRequired()])
    reason = StringField("Reason", validators=[DataRequired()])
    submit = SubmitField("Add Plan")

class SearchForm(FlaskForm):
    place = StringField("Search Place", validators=[DataRequired()])
    submit = SubmitField("Search")
