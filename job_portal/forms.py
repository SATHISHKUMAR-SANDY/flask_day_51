from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class ApplicationForm(FlaskForm):
    job_title = StringField("Job Title", validators=[DataRequired()])
    company = StringField("Company", validators=[DataRequired()])
    cover_letter = TextAreaField("Cover Letter", validators=[Length(min=10)])
    submit = SubmitField("Apply")
