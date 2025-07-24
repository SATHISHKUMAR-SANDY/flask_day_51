from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class BookForm(FlaskForm):
    title = StringField("Book Title", validators=[DataRequired(), Length(min=1)])
    pages_read = IntegerField("Pages Read", validators=[DataRequired()])
    submit = SubmitField("Add / Update")
